class OverallScoreCalculator:
    """
    Calculates the overall project score using weighted assessment scores.

    Weight Distribution
    -------------------
    Requirement   : 35%
    Security      : 25%
    Performance   : 20%
    Best Practice : 20%
    """

    WEIGHTS = {
        "requirement": 0.35,
        "security": 0.25,
        "performance": 0.20,
        "best_practice": 0.20,
    }

    MAX_SCORE = 100

    # ==========================================================
    # Calculate Overall Score
    # ==========================================================

    def calculate(
        self,
        requirement_assessment,
        security_assessment,
        performance_assessment,
        best_practice_assessment,
    ):
        """
        Calculates the weighted overall project score.

        Parameters
        ----------
        requirement_assessment : dict
        security_assessment : dict
        performance_assessment : dict
        best_practice_assessment : dict

        Returns
        -------
        dict
            Overall project score with detailed breakdown.
        """

        # ------------------------------------------------------
        # Raw Scores
        # ------------------------------------------------------

        raw_scores = {

            "requirement": (
                requirement_assessment["summary"]["confidence"]
            ),

            "security": (
                security_assessment["summary"]["security_score"]
            ),

            "performance": (
                performance_assessment["summary"]["performance_score"]
            ),

            "best_practice": (
                best_practice_assessment["summary"]["best_practice_score"]
            ),

        }

        # ------------------------------------------------------
        # Weighted Scores
        # ------------------------------------------------------

        weighted_scores = {}

        for category, score in raw_scores.items():

            weighted_scores[category] = round(
                score * self.WEIGHTS[category],
                2,
            )

        # ------------------------------------------------------
        # Overall Score
        # ------------------------------------------------------

        overall_score = round(
            sum(weighted_scores.values())
        )

        # ------------------------------------------------------
        # Return Result
        # ------------------------------------------------------

        return {

            "overall_score": overall_score,

            "max_score": self.MAX_SCORE,

            "raw_scores": raw_scores,

            "weighted_scores": weighted_scores,

            "weights": self.WEIGHTS,

        }