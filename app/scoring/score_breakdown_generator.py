class ScoreBreakdownGenerator:
    """
    Generates a detailed explanation of how the overall project
    score was calculated.
    """

    # ==========================================================
    # Generate Breakdown
    # ==========================================================

    def generate(self, grade_report):
        """
        Generates a detailed score breakdown.

        Parameters
        ----------
        grade_report : dict
            Output from ScoreGradeClassifier.

        Returns
        -------
        dict
            Detailed score breakdown.
        """

        score_report = grade_report["score_report"]

        raw_scores = score_report["raw_scores"]
        weighted_scores = score_report["weighted_scores"]
        weights = score_report["weights"]

        breakdown = []

        # ------------------------------------------------------
        # Category Breakdown
        # ------------------------------------------------------

        for category in raw_scores:

            category_name = category.replace(
                "_",
                " "
            ).title()

            breakdown.append({

                "category": category_name,

                "raw_score": raw_scores[category],

                "weight": weights[category],

                "weighted_score": weighted_scores[category],

                "explanation": (
                    f"{category_name} contributed "
                    f"{weighted_scores[category]} points "
                    f"({raw_scores[category]} × "
                    f"{weights[category]:.2f})."
                )

            })

        # ------------------------------------------------------
        # Return Report
        # ------------------------------------------------------

        return {

            "overall_score": score_report["overall_score"],

            "max_score": score_report["max_score"],

            "grade": grade_report["grade"],

            "grade_range": grade_report["grade_range"],

            "deployment_recommendation":
                grade_report["deployment_recommendation"],

            "summary": (
                f"Overall Score: "
                f"{score_report['overall_score']}/"
                f"{score_report['max_score']} "
                f"({grade_report['grade']})"
            ),

            "breakdown": breakdown,

        }