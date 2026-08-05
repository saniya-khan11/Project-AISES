import json


class EvaluationPrompt:

    def build(
        self,
        requirement,
        mapping,
        project
    ):

        requirement_json = json.dumps(
            requirement,
            indent=4,
            ensure_ascii=False
        )

        mapping_json = json.dumps(
            mapping,
            indent=4,
            ensure_ascii=False
        )

        project_json = json.dumps(
            project,
            indent=2,
            ensure_ascii=False
        )

        return f"""
You are an Expert Software Quality Assurance Engineer.

Your task is to evaluate whether the given Acceptance Criterion has been correctly implemented.

Acceptance Criterion

{requirement_json}

Mapping Information

{mapping_json}

Relevant Source Code and CST

{project_json}

Evaluation Instructions

1. Study the acceptance criterion carefully.
2. Analyze the mapped source code.
3. Determine whether the requirement is:
   - Implemented
   - Partially Implemented
   - Not Implemented
4. Explain your reasoning.
5. Identify missing logic.
6. Suggest improvements.

Return ONLY valid JSON.

Output Format

{{
    "ac_id":"",
    "status":"",
    "confidence":0,
    "coverage":0,
    "strengths":[],
    "missing_requirements":[],
    "issues":[],
    "recommendations":[],
    "reasoning":""
}}
"""