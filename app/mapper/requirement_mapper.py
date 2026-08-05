import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from app.agents.gemini_client import GeminiClient
from app.config.config_loader import ConfigLoader
from app.mapper.parser import MappingParser
from app.mapper.prompt import MappingPrompt


class RequirementMapper:
    """
    Maps acceptance criteria to relevant source files.

    Gemini-optimized features:
    - Does not send the complete CST to Gemini
    - Limits candidate files and source-code size
    - Saves progress after every acceptance criterion
    - Resumes existing mapping.json results
    - Retries malformed JSON responses
    - Removes invented filenames
    """

    def __init__(self) -> None:
        config = ConfigLoader()

        self.llm = GeminiClient()
        self.prompt = MappingPrompt()
        self.parser = MappingParser()

        self.max_candidate_files = int(
            config.get(
                "mapper_max_candidate_files",
                3,
            )
        )

        self.max_source_chars = int(
            config.get(
                "mapper_max_source_chars",
                20000,
            )
        )

        self.response_parse_retries = int(
            config.get(
                "mapper_response_parse_retries",
                2,
            )
        )

    def map(
        self,
        requirements_file: str,
        project_file: str,
        candidate_file: str,
        output_file: str = "outputs/mapping.json",
    ) -> List[Dict[str, Any]]:
        print("=" * 80)
        print("REQUIREMENT MAPPER")
        print("=" * 80)

        requirements = self._load_json(
            requirements_file
        )

        project = self._load_json(
            project_file
        )

        candidates = self._load_json(
            candidate_file
        )

        acceptance_criteria = requirements.get(
            "acceptance_criteria",
            [],
        )

        project_files = project.get(
            "files",
            [],
        )

        project_lookup = {
            file_data.get("file_id"): file_data
            for file_data in project_files
            if file_data.get("file_id")
        }

        candidate_lookup = {
            item.get("ac_id"): item
            for item in candidates
            if isinstance(item, dict)
            and item.get("ac_id")
        }

        mappings = self._load_existing_mappings(
            output_file
        )

        completed_ac_ids = {
            mapping.get("ac_id")
            for mapping in mappings
            if isinstance(mapping, dict)
            and mapping.get("ac_id")
        }

        if completed_ac_ids:
            print(
                f"Resuming with "
                f"{len(completed_ac_ids)} "
                "existing mappings."
            )

        total = len(acceptance_criteria)

        for index, ac in enumerate(
            acceptance_criteria,
            start=1,
        ):
            ac_id = str(
                ac.get(
                    "ac_id",
                    f"AC-{index:03d}",
                )
            )

            if ac_id in completed_ac_ids:
                print(
                    f"Skipping {ac_id}: already mapped."
                )
                continue

            print(
                f"\nMapping {ac_id} "
                f"({index}/{total})"
            )

            candidate = candidate_lookup.get(
                ac_id,
                {},
            )

            compact_project = (
                self._build_compact_project(
                    project=project,
                    candidate=candidate,
                    project_lookup=project_lookup,
                )
            )

            selected_files = compact_project.get(
                "files",
                [],
            )

            if not selected_files:
                print(
                    f"No candidate files found for {ac_id}."
                )

                mapping = self._empty_mapping(
                    ac_id=ac_id,
                    reasoning=(
                        "No candidate source files were "
                        "retrieved for this acceptance criterion."
                    ),
                )

                mappings.append(mapping)
                completed_ac_ids.add(ac_id)

                self._save_progress(
                    mappings,
                    output_file,
                )

                continue

            prompt = self.prompt.build(
                ac,
                compact_project,
            )

            print(
                f"Candidate files: "
                f"{len(selected_files)}"
            )

            print(
                f"Mapper prompt size: "
                f"{len(prompt):,} characters"
            )

            allowed_files = {
                str(file_data.get("filename"))
                for file_data in selected_files
                if file_data.get("filename")
            }

            try:
                mapping = self._request_mapping(
                    prompt=prompt,
                    ac_id=ac_id,
                    allowed_files=allowed_files,
                )

            except Exception as error:
                print(
                    f"Mapping failed for {ac_id}: "
                    f"{error}"
                )

                mapping = self._empty_mapping(
                    ac_id=ac_id,
                    reasoning=(
                        "Mapping could not be completed "
                        f"because of an error: {error}"
                    ),
                )

            mappings.append(mapping)
            completed_ac_ids.add(ac_id)

            # Save after every completed criterion.
            self._save_progress(
                mappings,
                output_file,
            )

        print()
        print(f"Saved : {output_file}")

        return mappings

    def _request_mapping(
        self,
        prompt: str,
        ac_id: str,
        allowed_files: Set[str],
    ) -> Dict[str, Any]:
        """
        Request and validate one mapping response.
        """

        total_attempts = max(
            1,
            self.response_parse_retries + 1,
        )

        last_error: Optional[Exception] = None
        current_prompt = prompt

        for attempt in range(
            1,
            total_attempts + 1,
        ):
            try:
                response = self.llm.ask(
                    current_prompt
                )

                parsed = self.parser.parse(
                    response
                )

                return self._normalize_mapping(
                    mapping=parsed,
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
                    f"Invalid JSON for {ac_id} "
                    f"(parse attempt "
                    f"{attempt}/{total_attempts}): "
                    f"{error}"
                )

                if attempt < total_attempts:
                    current_prompt = (
                        prompt
                        + "\n\n"
                        + """
IMPORTANT CORRECTION:

Return exactly one valid JSON object.

Do not use Markdown.
Do not use code fences.
Do not include comments.
Do not include any text before or after the JSON.
Use exactly the requested keys and value types.
"""
                    )

        raise RuntimeError(
            "Gemini did not return valid mapping JSON: "
            f"{last_error}"
        )

    def _build_compact_project(
        self,
        project: Dict[str, Any],
        candidate: Dict[str, Any],
        project_lookup: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Build a small project object without the large CST.
        """

        candidate_items = candidate.get(
            "candidate_files",
            [],
        )

        if not isinstance(candidate_items, list):
            candidate_items = []

        candidate_items = sorted(
            candidate_items,
            key=lambda item: (
                item.get("score", 0)
                if isinstance(item, dict)
                else 0
            ),
            reverse=True,
        )

        selected_files: List[Dict[str, Any]] = []

        for item in candidate_items[
            : self.max_candidate_files
        ]:
            if not isinstance(item, dict):
                continue

            file_id = item.get("file_id")

            file_data = project_lookup.get(
                file_id
            )

            if not file_data:
                continue

            parse_status = file_data.get(
                "parse_status"
            )

            if (
                parse_status
                and parse_status != "SUCCESS"
            ):
                continue

            source_code = str(
                file_data.get(
                    "source_code",
                    "",
                )
            )

            if not source_code.strip():
                continue

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
                    "extension": file_data.get(
                        "extension"
                    ),
                    "language": file_data.get(
                        "language"
                    ),
                    "candidate_score": item.get(
                        "score",
                        0,
                    ),
                    "source_code": (
                        self._limit_source_code(
                            source_code
                        )
                    ),
                }
            )

        return {
            "project": project.get(
                "project",
                {},
            ),
            "files": selected_files,
        }

    def _limit_source_code(
        self,
        source_code: str,
    ) -> str:
        """
        Keep the beginning and end of very large source files.
        """

        if (
            self.max_source_chars <= 0
            or len(source_code)
            <= self.max_source_chars
        ):
            return source_code

        marker = (
            "\n\n"
            "/* ... SOURCE TRUNCATED BY AISES ... */"
            "\n\n"
        )

        available = (
            self.max_source_chars
            - len(marker)
        )

        if available <= 0:
            return source_code[
                : self.max_source_chars
            ]

        beginning_size = int(
            available * 0.70
        )

        ending_size = (
            available
            - beginning_size
        )

        return (
            source_code[:beginning_size]
            + marker
            + source_code[-ending_size:]
        )

    def _normalize_mapping(
        self,
        mapping: Dict[str, Any],
        ac_id: str,
        allowed_files: Set[str],
    ) -> Dict[str, Any]:
        """
        Normalize values and remove filenames Gemini invented.
        """

        if not isinstance(mapping, dict):
            raise TypeError(
                "Mapping response must be a JSON object."
            )

        raw_files = mapping.get(
            "matched_files",
            [],
        )

        if not isinstance(raw_files, list):
            raw_files = []

        matched_files: List[str] = []

        for filename in raw_files:
            normalized_filename = str(
                filename
            ).strip()

            if (
                normalized_filename in allowed_files
                and normalized_filename
                not in matched_files
            ):
                matched_files.append(
                    normalized_filename
                )

        matched_nodes = mapping.get(
            "matched_nodes",
            [],
        )

        if not isinstance(matched_nodes, list):
            matched_nodes = []

        try:
            confidence = float(
                mapping.get(
                    "confidence",
                    0,
                )
            )
        except (
            TypeError,
            ValueError,
        ):
            confidence = 0.0

        confidence = max(
            0.0,
            min(
                100.0,
                confidence,
            ),
        )

        if confidence.is_integer():
            normalized_confidence: Any = int(
                confidence
            )
        else:
            normalized_confidence = round(
                confidence,
                2,
            )

        reasoning = str(
            mapping.get(
                "reasoning",
                "",
            )
        ).strip()

        return {
            "ac_id": ac_id,
            "matched_files": matched_files,
            "matched_nodes": matched_nodes,
            "confidence": normalized_confidence,
            "reasoning": reasoning,
        }

    @staticmethod
    def _empty_mapping(
        ac_id: str,
        reasoning: str,
    ) -> Dict[str, Any]:
        return {
            "ac_id": ac_id,
            "matched_files": [],
            "matched_nodes": [],
            "confidence": 0,
            "reasoning": reasoning,
        }

    def _load_existing_mappings(
        self,
        output_file: str,
    ) -> List[Dict[str, Any]]:
        """
        Load partial progress from an earlier run.
        """

        output_path = Path(output_file)

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

        except Exception as error:
            print(
                "Existing mapping file could not "
                f"be loaded: {error}"
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
        mappings: List[Dict[str, Any]],
        output_file: str,
    ) -> None:
        """
        Save atomically so an interrupted write does not
        corrupt mapping.json.
        """

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary_path = output_path.with_suffix(
            output_path.suffix + ".tmp"
        )

        with open(
            temporary_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                mappings,
                file,
                indent=4,
                ensure_ascii=False,
            )

        temporary_path.replace(
            output_path
        )