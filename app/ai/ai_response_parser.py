import json
import re


class AIResponseParser:
    """
    Parses and validates AI responses.

    Responsibilities
    ----------------
    - Remove markdown code fences.
    - Extract the JSON object.
    - Parse JSON.
    - Validate required fields.
    - Fill missing optional fields.
    """

    REQUIRED_FIELDS = [
        "summary",
        "strengths",
        "weaknesses",
        "suggestions",
        "final_assessment",
    ]

    OPTIONAL_DEFAULTS = {
        "confidence": 0,
        "reasoning": [],
    }

    # ==========================================================
    # Parse Response
    # ==========================================================

    def parse(self, response):
        """
        Parses the AI response into a validated dictionary.

        Parameters
        ----------
        response : str
            Raw response returned by the LLM.

        Returns
        -------
        dict
            Parsed AI response.
        """

        cleaned_response = self._clean_response(response)

        try:
            data = json.loads(cleaned_response)

        except json.JSONDecodeError as ex:
            raise ValueError(
                f"Invalid JSON returned by AI: {ex}"
            )

        self._validate_required_fields(data)

        # Add default values for optional fields
        for key, default in self.OPTIONAL_DEFAULTS.items():
            data.setdefault(key, default)

        return data

    # ==========================================================
    # Clean Response
    # ==========================================================

    def _clean_response(self, response):
        """
        Removes markdown code fences and extracts the JSON object.
        """

        response = response.strip()

        # Remove markdown code fences
        response = re.sub(
            r"```(?:json)?",
            "",
            response,
            flags=re.IGNORECASE,
        )

        response = response.replace("```", "")

        # Extract first JSON object
        match = re.search(
            r"\{.*\}",
            response,
            flags=re.DOTALL,
        )

        if not match:
            raise ValueError(
                "No JSON object found in AI response."
            )

        return match.group(0).strip()

    # ==========================================================
    # Validate Required Fields
    # ==========================================================

    def _validate_required_fields(self, data):
        """
        Ensures all required fields exist.
        """

        missing = []

        for field in self.REQUIRED_FIELDS:
            if field not in data:
                missing.append(field)

        if missing:
            raise ValueError(
                "Missing required field(s): "
                + ", ".join(missing)
            )