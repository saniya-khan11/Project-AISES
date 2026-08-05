import json
import re
from typing import Any, Dict


class EvaluationParser:
    """
    Parses and validates Gemini evaluator responses.
    """

    def parse(self, response: str) -> Dict[str, Any]:
        if not isinstance(response, str):
            raise TypeError(
                "Evaluation response must be a string."
            )

        cleaned = response.strip()

        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "No complete JSON object was found "
                "in the evaluation response."
            )

        json_text = cleaned[start:end + 1]

        parsed = json.loads(json_text)

        if not isinstance(parsed, dict):
            raise TypeError(
                "Parsed evaluation data must be a JSON object."
            )

        return parsed