import json
import re


class ResponseParser:
    """
    Cleans and parses LLM responses.
    """

    def parse(self, response):

        response = response.strip()

        response = re.sub(
            r"^```json",
            "",
            response,
            flags=re.IGNORECASE,
        )

        response = re.sub(
            r"^```",
            "",
            response,
        )

        response = re.sub(
            r"```$",
            "",
            response,
        )

        response = response.strip()

        return json.loads(response)