class ExtraFeaturePrompt:

    def build(
        self,
        requirement,
        capability,
    ):

        prompt = f"""
You are an expert Software Architect.

Requirement

{requirement.description}

Implemented Business Capability

Primary Capability:
{capability.primary_capability}

Sub Capabilities:
{chr(10).join("- " + x for x in capability.sub_capabilities)}

Task

Identify

1. Which sub-capabilities are REQUIRED.

2. Which sub-capabilities are EXTRA.

3. Explain why.

Return ONLY JSON.

Example

{{
    "required":[...],
    "extra":[...],
    "reasoning":[...]
}}
"""

        return prompt