class EvaluationContext:
    """
    Builds the evaluation context supplied to the AI.

    Responsibilities
    ----------------
    - Collect outputs from all assessment modules.
    - Build a single structured context object.
    """

    def build(
        self,
        requirement_assessment,
        security_assessment,
        performance_assessment,
        best_practice_assessment,
        project_name=None,
    ):

        context = {

            "project": {
                "name": project_name or "Unknown Project"
            },

            "requirement": requirement_assessment,

            "security": security_assessment,

            "performance": performance_assessment,

            "best_practice": best_practice_assessment,

        }

        return context