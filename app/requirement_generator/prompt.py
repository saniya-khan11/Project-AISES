class RequirementPrompt:

    def build(self, srs_text: str):

        return f"""
You are a Senior Software Architect and Software Requirements Engineer.

Analyze the following Software Requirements Specification (SRS).

Your task is to extract EVERY functional requirement and decompose each requirement into ATOMIC Acceptance Criteria.

Rules:

1. Every Acceptance Criterion (AC) must represent exactly ONE observable behavior.
2. Generate unique sequential IDs.
3. Do NOT invent requirements.
4. Do NOT omit any functional requirement.
5. Acceptance Criteria should be implementation-independent.
6. Generate implementation keywords that may help locate the corresponding source code.
7. Return ONLY valid JSON.

Requirement IDs:

REQ-001
REQ-002
...

Acceptance Criteria IDs:

AC-001
AC-002
...

Output JSON Schema

{{
    "project_name": "",
    "project_description": "",

    "acceptance_criteria": [

        {{

            "ac_id": "",

            "requirement_id": "",

            "requirement_title": "",

            "description": "",

            "priority": "",

            "inputs": [],

            "expected_outputs": [],

            "preconditions": [],

            "postconditions": [],

            "keywords": []

        }}

    ]
}}

SRS

{srs_text}
"""