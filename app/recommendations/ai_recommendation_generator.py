from app.ai.llm_manager import LLMManager
from app.ai.prompt_builder import PromptBuilder


class AIRecommendationGenerator:
    """
    Generates AI-powered software engineering recommendations
    using the LLM.
    """

    def __init__(self):

        self.llm = LLMManager()

        self.builder = PromptBuilder()

    # ==========================================================
    # Generate AI Recommendations
    # ==========================================================

    def generate(self, assessment):
        """
        Parameters
        ----------
        assessment : dict
            Complete assessment context.

        Returns
        -------
        list
            AI-generated recommendations.
        """

        prompt = self.builder.build(

            role="Senior Software Architect",

            task="""
Generate implementation recommendations based on the supplied
software assessment.

Recommendations may include:

1. Missing requirement implementation
2. Removal of extra functionality
3. Security improvements
4. Performance improvements
5. Best practice improvements
6. Refactoring suggestions

Return ONLY valid JSON.
""",

            context=assessment,

            output_schema={
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

        )

        response = self.llm.ask(prompt)

        if not response.success:
            return []

        data = response.parsed_data

        return data.get("recommendations", [])