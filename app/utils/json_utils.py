import json
import re


class JSONUtils:

    @staticmethod
    def extract_json(text: str):

        # Remove markdown code fences
        text = text.replace("```json", "")
        text = text.replace("```", "")

        # Find first JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            raise ValueError("No JSON object found.")

        return json.loads(match.group())