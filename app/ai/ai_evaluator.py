from app.ai.ollama_client import OllamaClient
from app.ai.prompt_builder import PromptBuilder


class AIEvaluator:
    """
    Executes the AI evaluation workflow.

    Responsibilities
    ----------------
    - Build the prompt.
    - Send the prompt to Ollama.
    - Return the raw AI response.
    """

    def __init__(self, model="qwen2.5-coder:7b"):

        self.prompt_builder = PromptBuilder()
        self.client = OllamaClient(model=model)

    # ==========================================================
    # Evaluate
    # ==========================================================

    def evaluate(self, context):
        """
        Executes the AI evaluation.

        Parameters
        ----------
        context : dict
            Evaluation context.

        Returns
        -------
        dict
        """

        prompt = self.prompt_builder.build(context)

        response = self.client.generate(prompt)

        return {

            "prompt": prompt,

            "response": response

        }