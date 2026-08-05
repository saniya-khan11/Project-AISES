import json


class PromptBuilder:
    """
    Generic prompt builder for all AISES AI modules.
    """

    def build(
        self,
        role: str,
        task: str,
        context,
        output_schema: dict,
        rules=None,
    ):

        if rules is None:
            rules = [
                "Respond ONLY with valid JSON.",
                "Do not include markdown.",
                "Do not include explanations.",
                "Do not invent information.",
                "Use only the supplied context."
            ]

        context_text = json.dumps(
            context,
            indent=4,
            ensure_ascii=False
        )

        schema_text = json.dumps(
            output_schema,
            indent=4,
            ensure_ascii=False
        )

        prompt = f"""
ROLE

{role}

==========================================================
TASK
==========================================================

{task}

==========================================================
CONTEXT
==========================================================

{context_text}

==========================================================
OUTPUT JSON
==========================================================

{schema_text}

==========================================================
RULES
==========================================================

"""

        for i, rule in enumerate(rules, start=1):
            prompt += f"{i}. {rule}\n"

        return prompt.strip()