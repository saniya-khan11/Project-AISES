import json


class MappingPrompt:

    def build(
        self,
        acceptance_criterion,
        project_cst
    ):

        ac_json = json.dumps(
            acceptance_criterion,
            indent=4,
            ensure_ascii=False
        )

        project_json = json.dumps(
            project_cst,
            indent=2,
            ensure_ascii=False
        )

        return f"""
You are an Expert Software Traceability Engineer.

==============================================================================
OBJECTIVE
==============================================================================

Your task is to identify which of the PROVIDED source files
contain evidence that implements the given Acceptance Criterion.

You are NOT allowed to guess.

You are NOT allowed to invent filenames.

You are NOT allowed to assume hidden code exists.

You MUST ONLY use the supplied project files.

==============================================================================
ACCEPTANCE CRITERION
==============================================================================

{ac_json}

==============================================================================
PROJECT FILES
==============================================================================

{project_json}

==============================================================================
RULES
==============================================================================

1. Read the Acceptance Criterion carefully.

2. Examine ONLY the supplied project files.

3. Select ONLY files that contain direct evidence
   of implementing the requirement.

4. Never invent filenames.

5. Never invent classes.

6. Never invent methods.

7. Never refer to files not present in the supplied project.

8. If no evidence exists,
   return an empty matched_files list.

9. Confidence should represent ONLY
   how certain you are are based on the supplied evidence.

10. Reasoning must clearly explain WHY each selected file
    satisfies the requirement.

11. If you are uncertain, return an empty list instead of guessing.

==============================================================================
OUTPUT FORMAT
==============================================================================

Return ONLY valid JSON.

Do NOT include markdown.

Do NOT include explanations.

Do NOT include ```json.

Return EXACTLY in the following format:

{{
    "ac_id": "",
    "matched_files": [
        "filename1",
        "filename2"
    ],
    "matched_nodes": [],
    "confidence": 0,
    "reasoning": ""
}}
"""