import json
import re
from typing import Any, Dict


class RequirementParser:
    """
    Parses and validates Gemini requirement-generator responses.
    """

    def parse(self, response: str) -> Dict[str, Any]:
        if not isinstance(response, str):
            raise TypeError(
                "Requirement response must be a string."
            )

        cleaned = response.strip()

        # Remove optional Markdown fences.
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

        # Extract the outer JSON object.
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "No complete JSON object was found "
                "in the Gemini response."
            )

        json_text = cleaned[start:end + 1]

        parsed = json.loads(json_text)

        if not isinstance(parsed, dict):
            raise TypeError(
                "Parsed requirement data must be a JSON object."
            )

        return parsed