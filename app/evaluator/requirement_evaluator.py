import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from app.agents.gemini_client import GeminiClient
from app.config.config_loader import ConfigLoader
from app.evaluator.parser import EvaluationParser


class RequirementEvaluator:
    """
    Evaluates each acceptance criterion against relevant source code.

    This version:
    - Never sends the complete CST to Gemini
    - Sends only files mapped to the current acceptance criterion
    - Limits source-code size
    - Validates Gemini output
    - Saves progress after every evaluation
    - Resumes from an existing evaluation.json file
    - Prevents invented filenames
    """

    VALID_STATUSES = {
        "Implemented",
        "Partially Implemented",
        "Not Implemented",
    }

    def __init__(self) -> None:
        config = ConfigLoader()

        self.llm = GeminiClient()
        self.parser = EvaluationParser()

        self.max_files = int(
            config.get(
                "evaluator_max_files",
                3,
            )
        )

        self.max_source_chars_per_file = int(
            config.get(
                "evaluator_max_source_chars_per_file",
                12000,
            )
        )

        self.max_total_source_chars = int(
            config.get(
                "evaluator_max_total_source_chars",
                24000,
            )
        )

        self.parse_retries = int(
            config.get(
                "evaluator_response_parse_retries",
                2,
            )
        )

    def evaluate(
        self,
        requirements_file: str,
        mapping_file: str,
        project_file: str,
        output_file: str = "outputs/evaluation.json",
    ) -> List[Dict[str, Any]]:
        print("=" * 80)
        print("REQUIREMENT EVALUATOR")
        print("=" * 80)

        requirements = self._load_json(
            requirements_file
        )

        mappings = self._load_json(
            mapping_file
        )

        project = self._load_json(
            project_file
        )

        acceptance_criteria = requirements.get(
            "acceptance_criteria",
            [],
        )

        if not isinstance(
            acceptance_criteria,
            list,
        ):
            raise ValueError(
                "'acceptance_criteria' must be a list."
            )

        mapping_lookup = self._build_mapping_lookup(
            mappings
        )

        project_lookup = self._build_project_lookup(
            project
        )

        evaluations = self._load_existing_evaluations(
            output_file
        )

        completed_ac_ids = {
            str(item.get("ac_id"))
            for item in evaluations
            if isinstance(item, dict)
            and item.get("ac_id")
        }

        if completed_ac_ids:
            print(
                f"Resuming with "
                f"{len(completed_ac_ids)} "
                "existing evaluations."
            )

        total = len(acceptance_criteria)

        for index, criterion in enumerate(
            acceptance_criteria,
            start=1,
        ):
            ac_id = self._get_ac_id(
                criterion,
                index,
            )

            if ac_id in completed_ac_ids:
                print(
                    f"Skipping {ac_id}: already evaluated."
                )
                continue

            print()
            print(
                f"Evaluating {ac_id} "
                f"({index}/{total})"
            )

            mapping = mapping_lookup.get(
                ac_id,
                {},
            )

            relevant_files = self._collect_relevant_files(
                mapping=mapping,
                project_lookup=project_lookup,
            )

            if not relevant_files:
                print(
                    f"No mapped source files found "
                    f"for {ac_id}."
                )

                evaluation = self._empty_evaluation(
                    ac_id=ac_id,
                    reason=(
                        "No source files were mapped to this "
                        "acceptance criterion."
                    ),
                )

                evaluations.append(evaluation)
                completed_ac_ids.add(ac_id)

                self._save_progress(
                    evaluations,
                    output_file,
                )

                continue

            prompt = self._build_prompt(
                criterion=criterion,
                mapping=mapping,
                relevant_files=relevant_files,
                ac_id=ac_id,
            )

            print(
                f"Relevant files : "
                f"{len(relevant_files)}"
            )

            print(
                f"Evaluator prompt size: "
                f"{len(prompt):,} characters"
            )

            allowed_files = {
                str(file_data.get("filename"))
                for file_data in relevant_files
                if file_data.get("filename")
            }

            try:
                evaluation = self._request_evaluation(
                    prompt=prompt,
                    ac_id=ac_id,
                    allowed_files=allowed_files,
                )

            except Exception as error:
                print(
                    f"Evaluation failed for "
                    f"{ac_id}: {error}"
                )

                evaluation = self._empty_evaluation(
                    ac_id=ac_id,
                    reason=(
                        "The acceptance criterion could not "
                        f"be evaluated because of an error: "
                        f"{error}"
                    ),
                )

            evaluations.append(evaluation)
            completed_ac_ids.add(ac_id)

            self._save_progress(
                evaluations,
                output_file,
            )

        print()
        print(f"Saved : {output_file}")

        return evaluations

    def _request_evaluation(
        self,
        prompt: str,
        ac_id: str,
        allowed_files: Set[str],
    ) -> Dict[str, Any]:
        """
        Send an evaluation prompt and validate its JSON response.
        """

        attempts = max(
            1,
            self.parse_retries + 1,
        )

        current_prompt = prompt
        last_error: Optional[Exception] = None

        for attempt in range(
            1,
            attempts + 1,
        ):
            try:
                response = self.llm.ask(
                    current_prompt
                )

                parsed = self.parser.parse(
                    response
                )

                return self._normalize_evaluation(
                    evaluation=parsed,
                    ac_id=ac_id,
                    allowed_files=allowed_files,
                )

            except (
                json.JSONDecodeError,
                TypeError,
                ValueError,
                KeyError,
            ) as error:
                last_error = error

                print(
                    f"Invalid evaluation JSON for "
                    f"{ac_id} "
                    f"(parse attempt "
                    f"{attempt}/{attempts}): "
                    f"{error}"
                )

                if attempt < attempts:
                    current_prompt = (
                        prompt
                        + "\n\n"
                        + """
CORRECTION:

Your previous answer was not valid JSON.

Return exactly one complete JSON object.
Do not use Markdown fences.
Do not add comments.
Do not add explanations outside the JSON.
Close every string, list, and object.
Keep all text fields concise.
"""
                    )

        raise RuntimeError(
            "Gemini did not return valid evaluation JSON: "
            f"{last_error}"
        )

    def _collect_relevant_files(
        self,
        mapping: Dict[str, Any],
        project_lookup: Dict[str, Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Collect only mapped source files.

        CST data is intentionally excluded.
        """

        mapped_names = self._extract_mapped_filenames(
            mapping
        )

        selected_files: List[Dict[str, Any]] = []
        total_chars = 0

        for filename in mapped_names[
            : self.max_files
        ]:
            file_data = project_lookup.get(
                filename
            )

            if not file_data:
                continue

            source_code = str(
                file_data.get(
                    "source_code",
                    "",
                )
            )

            if not source_code.strip():
                continue

            remaining_chars = (
                self.max_total_source_chars
                - total_chars
            )

            if remaining_chars <= 0:
                break

            file_limit = min(
                self.max_source_chars_per_file,
                remaining_chars,
            )

            limited_source = self._limit_text(
                source_code,
                file_limit,
            )

            selected_files.append(
                {
                    "file_id": file_data.get(
                        "file_id"
                    ),
                    "filename": file_data.get(
                        "filename"
                    ),
                    "path": file_data.get(
                        "path"
                    ),
                    "language": file_data.get(
                        "language"
                    ),
                    "source_code": limited_source,
                }
            )

            total_chars += len(
                limited_source
            )

        return selected_files

    @staticmethod
    def _extract_mapped_filenames(
        mapping: Dict[str, Any],
    ) -> List[str]:
        """
        Support common mapping formats.
        """

        possible_values = [
            mapping.get("matched_files"),
            mapping.get("mapped_files"),
            mapping.get("files"),
            mapping.get("candidate_files"),
        ]

        filenames: List[str] = []

        for value in possible_values:
            if not isinstance(value, list):
                continue

            for item in value:
                filename: Optional[str] = None

                if isinstance(item, str):
                    filename = item

                elif isinstance(item, dict):
                    filename = (
                        item.get("filename")
                        or item.get("file_name")
                        or item.get("path")
                    )

                if filename:
                    filename = Path(
                        str(filename)
                    ).name

                    if filename not in filenames:
                        filenames.append(filename)

        return filenames

    def _build_prompt(
        self,
        criterion: Dict[str, Any],
        mapping: Dict[str, Any],
        relevant_files: List[Dict[str, Any]],
        ac_id: str,
    ) -> str:
        """
        Build a compact evaluator prompt.

        Only the current criterion, compact mapping metadata,
        and relevant source code are included.
        """

        criterion_text = self._get_criterion_text(
            criterion
        )

        mapped_nodes = mapping.get(
            "matched_nodes",
            [],
        )

        if not isinstance(mapped_nodes, list):
            mapped_nodes = []

        compact_nodes = mapped_nodes[:20]

        source_sections: List[str] = []

        for file_data in relevant_files:
            source_sections.append(
                "\n".join(
                    [
                        (
                            "FILE: "
                            f"{file_data.get('filename', '')}"
                        ),
                        (
                            "LANGUAGE: "
                            f"{file_data.get('language', '')}"
                        ),
                        "SOURCE CODE:",
                        str(
                            file_data.get(
                                "source_code",
                                "",
                            )
                        ),
                    ]
                )
            )

        source_text = "\n\n".join(
            source_sections
        )

        mapping_summary = {
            "matched_files": [
                file_data.get("filename")
                for file_data in relevant_files
            ],
            "matched_nodes": compact_nodes,
            "mapping_confidence": mapping.get(
                "confidence",
                0,
            ),
            "mapping_reasoning": mapping.get(
                "reasoning",
                "",
            ),
        }

        return f"""
You are evaluating whether source code satisfies one software acceptance criterion.

Evaluate only the implementation visible in the provided source code.
Do not assume missing behavior exists.
Do not mark a requirement implemented merely because comments claim it exists.
Base the decision on executable code.

ACCEPTANCE CRITERION ID:
{ac_id}

ACCEPTANCE CRITERION:
{criterion_text}

MAPPING SUMMARY:
{json.dumps(mapping_summary, ensure_ascii=False, indent=2)}

RELEVANT SOURCE FILES:
{source_text}

Return exactly one JSON object with this structure:

{{
  "ac_id": "{ac_id}",
  "status": "Implemented | Partially Implemented | Not Implemented",
  "coverage": 0,
  "confidence": 0,
  "matched_files": [],
  "strengths": [],
  "issues": [],
  "recommendations": [],
  "reasoning": ""
}}

Rules:

1. status must be exactly one of:
   "Implemented"
   "Partially Implemented"
   "Not Implemented"

2. coverage must be an integer from 0 to 100.

3. confidence must be an integer from 0 to 100.

4. matched_files may contain only filenames included above.

5. strengths, issues, and recommendations must be JSON arrays of short strings.

6. reasoning must briefly explain the decision using actual code evidence.

7. Return JSON only. Do not use Markdown.
""".strip()

    def _normalize_evaluation(
        self,
        evaluation: Dict[str, Any],
        ac_id: str,
        allowed_files: Set[str],
    ) -> Dict[str, Any]:
        """
        Normalize Gemini output into a stable schema.
        """

        if not isinstance(evaluation, dict):
            raise TypeError(
                "Evaluation response must be a JSON object."
            )

        status = str(
            evaluation.get(
                "status",
                "Not Implemented",
            )
        ).strip()

        status_lookup = {
            item.lower(): item
            for item in self.VALID_STATUSES
        }

        status = status_lookup.get(
            status.lower(),
            "Not Implemented",
        )

        coverage = self._bounded_integer(
            evaluation.get(
                "coverage",
                0,
            )
        )

        confidence = self._bounded_integer(
            evaluation.get(
                "confidence",
                0,
            )
        )

        raw_files = evaluation.get(
            "matched_files",
            [],
        )

        if not isinstance(raw_files, list):
            raw_files = []

        matched_files: List[str] = []

        for filename in raw_files:
            normalized_name = Path(
                str(filename)
            ).name

            if (
                normalized_name in allowed_files
                and normalized_name
                not in matched_files
            ):
                matched_files.append(
                    normalized_name
                )

        strengths = self._string_list(
            evaluation.get(
                "strengths",
                [],
            )
        )

        issues = self._string_list(
            evaluation.get(
                "issues",
                [],
            )
        )

        recommendations = self._string_list(
            evaluation.get(
                "recommendations",
                [],
            )
        )

        reasoning = str(
            evaluation.get(
                "reasoning",
                "",
            )
        ).strip()

        return {
            "ac_id": ac_id,
            "status": status,
            "coverage": coverage,
            "confidence": confidence,
            "matched_files": matched_files,
            "strengths": strengths,
            "issues": issues,
            "recommendations": recommendations,
            "reasoning": reasoning,
        }

    @staticmethod
    def _get_ac_id(
        criterion: Dict[str, Any],
        index: int,
    ) -> str:
        return str(
            criterion.get("ac_id")
            or criterion.get("id")
            or criterion.get("criterion_id")
            or f"AC-{index:03d}"
        )

    @staticmethod
    def _get_criterion_text(
        criterion: Dict[str, Any],
    ) -> str:
        values = [
            criterion.get("description"),
            criterion.get("criterion"),
            criterion.get("acceptance_criterion"),
            criterion.get("text"),
            criterion.get("requirement"),
            criterion.get("title"),
        ]

        text_parts = [
            str(value).strip()
            for value in values
            if value
            and str(value).strip()
        ]

        if text_parts:
            return "\n".join(
                dict.fromkeys(text_parts)
            )

        return json.dumps(
            criterion,
            ensure_ascii=False,
        )

    @staticmethod
    def _build_mapping_lookup(
        mappings: Any,
    ) -> Dict[str, Dict[str, Any]]:
        if isinstance(mappings, dict):
            possible_list = (
                mappings.get("mappings")
                or mappings.get("validated_mappings")
                or mappings.get("results")
            )

            if isinstance(possible_list, list):
                mappings = possible_list

            else:
                mappings = [
                    value
                    for value in mappings.values()
                    if isinstance(value, dict)
                ]

        if not isinstance(mappings, list):
            mappings = []

        result: Dict[str, Dict[str, Any]] = {}

        for item in mappings:
            if not isinstance(item, dict):
                continue

            ac_id = (
                item.get("ac_id")
                or item.get("id")
                or item.get("criterion_id")
            )

            if ac_id:
                result[str(ac_id)] = item

        return result

    @staticmethod
    def _build_project_lookup(
        project: Dict[str, Any],
    ) -> Dict[str, Dict[str, Any]]:
        files = project.get(
            "files",
            [],
        )

        if not isinstance(files, list):
            files = []

        lookup: Dict[str, Dict[str, Any]] = {}

        for file_data in files:
            if not isinstance(file_data, dict):
                continue

            filename = file_data.get(
                "filename"
            )

            if filename:
                lookup[
                    Path(str(filename)).name
                ] = file_data

        return lookup

    @staticmethod
    def _bounded_integer(
        value: Any,
    ) -> int:
        try:
            number = int(
                float(value)
            )
        except (
            TypeError,
            ValueError,
        ):
            number = 0

        return max(
            0,
            min(
                100,
                number,
            ),
        )

    @staticmethod
    def _string_list(
        value: Any,
    ) -> List[str]:
        if isinstance(value, str):
            value = [value]

        if not isinstance(value, list):
            return []

        result: List[str] = []

        for item in value:
            text = str(item).strip()

            if text and text not in result:
                result.append(text)

        return result

    @staticmethod
    def _limit_text(
        text: str,
        maximum_chars: int,
    ) -> str:
        if (
            maximum_chars <= 0
            or len(text) <= maximum_chars
        ):
            return text

        marker = (
            "\n\n"
            "# ... SOURCE TRUNCATED BY AISES ...\n\n"
        )

        available = (
            maximum_chars
            - len(marker)
        )

        if available <= 0:
            return text[
                :maximum_chars
            ]

        beginning_size = int(
            available * 0.75
        )

        ending_size = (
            available
            - beginning_size
        )

        return (
            text[:beginning_size]
            + marker
            + text[-ending_size:]
        )

    @staticmethod
    def _empty_evaluation(
        ac_id: str,
        reason: str,
    ) -> Dict[str, Any]:
        return {
            "ac_id": ac_id,
            "status": "Not Implemented",
            "coverage": 0,
            "confidence": 100,
            "matched_files": [],
            "strengths": [],
            "issues": [reason],
            "recommendations": [
                (
                    "Provide or correctly map the relevant "
                    "source implementation."
                )
            ],
            "reasoning": reason,
        }

    def _load_existing_evaluations(
        self,
        output_file: str,
    ) -> List[Dict[str, Any]]:
        output_path = Path(
            output_file
        )

        if not output_path.exists():
            return []

        try:
            existing = self._load_json(
                output_file
            )

            if isinstance(existing, list):
                return [
                    item
                    for item in existing
                    if isinstance(item, dict)
                ]

            if isinstance(existing, dict):
                possible_list = (
                    existing.get("evaluations")
                    or existing.get("results")
                )

                if isinstance(
                    possible_list,
                    list,
                ):
                    return [
                        item
                        for item in possible_list
                        if isinstance(item, dict)
                    ]

        except Exception as error:
            print(
                "Existing evaluation file could "
                f"not be loaded: {error}"
            )

        return []

    @staticmethod
    def _load_json(
        file_path: str,
    ) -> Any:
        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    @staticmethod
    def _save_progress(
        evaluations: List[Dict[str, Any]],
        output_file: str,
    ) -> None:
        output_path = Path(
            output_file
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_path = output_path.with_suffix(
            output_path.suffix + ".tmp"
        )

        with temporary_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                evaluations,
                file,
                indent=4,
                ensure_ascii=False,
            )

        temporary_path.replace(
            output_path
        )