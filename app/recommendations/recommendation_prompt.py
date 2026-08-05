class RecommendationPrompt:

    def build(
        self,
        assessment,
    ):

        return {

            "role": "Senior Software Architect",

            "task": (
                "Generate implementation recommendations."
            ),

            "context": assessment,

            "output_schema": {

                "recommendations": [

                    {

                        "title": "",

                        "description": "",

                        "priority": "",

                        "category": "",

                        "impact": "",

                        "code_location": "",

                        "suggested_fix": "",

                        "reasoning": ""

                    }

                ]

            }

        }