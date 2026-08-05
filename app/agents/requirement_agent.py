from app.agents.base_agent import BaseAgent


class RequirementAgent(BaseAgent):

    def build_prompt(
        self,
        task_context,
        task_description,
        acceptance_criteria,
        difficulty
    ):

        prompt = f"""
You are an expert Software Requirements Engineer.

Your task is to analyze a software development task and convert it into structured JSON.

Return ONLY valid JSON.

Schema:

{{
  "task_context": "",
  "task_summary": "",
  "difficulty": {{
      "level": 0,
      "label": ""
  }},
  "acceptance_criteria": [],
  "functional_requirements": [],
  "non_functional_requirements": []
}}

Task Context:
{task_context}

Task Description:
{task_description}

Acceptance Criteria:
{acceptance_criteria}

Difficulty:
{difficulty}
"""

        return prompt

    def extract(
        self,
        task_context,
        task_description,
        acceptance_criteria,
        difficulty
    ):

        prompt = self.build_prompt(
            task_context,
            task_description,
            acceptance_criteria,
            difficulty
        )

        return self.ask(prompt)