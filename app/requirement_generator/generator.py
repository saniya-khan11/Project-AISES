import json
from pathlib import Path
from typing import Any, Dict, Optional

from app.agents.gemini_client import GeminiClient
from app.requirement_generator.parser import RequirementParser
from app.requirement_generator.prompt import RequirementPrompt


class RequirementGenerator:
    """
    Generates structured requirements from an SRS file.

    Retries when Gemini returns malformed or incomplete JSON.
    """

    def __init__(self) -> None:
        self.llm = GeminiClient()
        self.prompt = RequirementPrompt()
        self.parser = RequirementParser()
        self.parse_retries = 3

    def generate(
        self,
        srs_file: str,
        output_file: str = "outputs/requirements.json",
    ) -> Dict[str, Any]:
        print("=" * 80)
        print("AISES REQUIREMENT GENERATOR")
        print("=" * 80)
        print("Generating structured requirements...")

        srs_text = Path(srs_file).read_text(
            encoding="utf-8"
        )

        original_prompt = self.prompt.build(
            srs_text
        )

        current_prompt = original_prompt
        last_error: Optional[Exception] = None

        for attempt in range(
            1,
            self.parse_retries + 1,
        ):
            try:
                response = self.llm.ask(
                    current_prompt
                )

                data = self.parser.parse(
                    response
                )

                if not isinstance(data, dict):
                    raise TypeError(
                        "Requirement response must be "
                        "a JSON object."
                    )

                acceptance_criteria = data.get(
                    "acceptance_criteria"
                )

                if not isinstance(
                    acceptance_criteria,
                    list,
                ):
                    raise ValueError(
                        "The response does not contain a valid "
                        "'acceptance_criteria' list."
                    )

                self._save_json(
                    data,
                    output_file,
                )

                print(f"Saved : {output_file}")
                return data

            except (
                json.JSONDecodeError,
                TypeError,
                ValueError,
                KeyError,
            ) as error:
                last_error = error

                print(
                    f"Invalid requirement JSON "
                    f"(attempt {attempt}/{self.parse_retries}): "
                    f"{error}"
                )

                if attempt < self.parse_retries:
                    current_prompt = (
                        original_prompt
                        + "\n\n"
                        + """
IMPORTANT CORRECTION:

Your previous response was incomplete or invalid JSON.

Return exactly one complete JSON object.
Do not use Markdown code fences.
Do not include explanations or comments.
Do not place any text before or after the JSON.
Close every string, array, and object.
Keep requirement and acceptance-criterion descriptions concise.
"""
                    )

        raise RuntimeError(
            "Requirement generation failed because Gemini "
            "did not return valid JSON after "
            f"{self.parse_retries} attempts: {last_error}"
        )

    @staticmethod
    def _save_json(
        data: Dict[str, Any],
        output_file: str,
    ) -> None:
        output_path = Path(output_file)

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
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        temporary_path.replace(
            output_path
        )