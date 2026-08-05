import json
import re


class ExtraFeatureParser:

    def parse(self, response):

        # Remove Markdown code fences
        response = response.strip()

        response = re.sub(
            r"^```json\s*",
            "",
            response,
            flags=re.IGNORECASE
        )

        response = re.sub(
            r"^```",
            "",
            response
        )

        response = re.sub(
            r"```$",
            "",
            response
        )

        response = response.strip()

        try:

            return json.loads(response)

        except Exception as e:

            print("\nJSON Parsing Error")
            print(e)

            print("\nReceived Response\n")
            print(response)

            return {

                "required": [],

                "extra": [],

                "reasoning": []
            }