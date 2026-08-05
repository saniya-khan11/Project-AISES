from app.ai.ai_evaluator import AIEvaluator
from app.ai.ai_response_parser import AIResponseParser
from app.ai.evaluation_context import EvaluationContext


class EvaluationAgent:
    """
    AI Evaluation Agent.

    Responsibilities
    ----------------
    - Build evaluation context.
    - Execute AI evaluation.
    - Parse and validate AI response.
    - Return the final structured evaluation.
    """

    def __init__(self, model="qwen2.5-coder:7b"):

        self.context_builder = EvaluationContext()
        self.evaluator = AIEvaluator(model=model)
        self.parser = AIResponseParser()

    # ==========================================================
    # Evaluate
    # ==========================================================

    def evaluate(
        self,
        requirement_assessment,
        security_assessment,
        performance_assessment,
        best_practice_assessment,
        project_name="Unknown Project",
    ):
        """
        Executes the complete AI evaluation pipeline.

        Parameters
        ----------
        requirement_assessment : dict

        security_assessment : dict

        performance_assessment : dict

        best_practice_assessment : dict

        project_name : str

        Returns
        -------
        dict
        """

        # ------------------------------------------------------
        # Build Context
        # ------------------------------------------------------

        context = self.context_builder.build(
            requirement_assessment,
            security_assessment,
            performance_assessment,
            best_practice_assessment,
            project_name=project_name,
        )

        # ------------------------------------------------------
        # Execute AI Evaluation
        # ------------------------------------------------------

        ai_result = self.evaluator.evaluate(context)

        # ------------------------------------------------------
        # Parse AI Response
        # ------------------------------------------------------

        parsed = self.parser.parse(
            ai_result["response"]
        )

        # ------------------------------------------------------
        # Final Report
        # ------------------------------------------------------

        return {

            "project": context["project"],

            "context": context,

            "prompt": ai_result["prompt"],

            "raw_response": ai_result["response"],

            "evaluation": parsed

        }