class ScoreGradeClassifier:
    """
    Classifies the overall project score into a quality grade.

    Score Range
    -----------
    90 - 100 : EXCELLENT
    80 - 89  : VERY GOOD
    70 - 79  : GOOD
    60 - 69  : FAIR
    40 - 59  : POOR
    0  - 39  : CRITICAL
    """

    # ==========================================================
    # Classify
    # ==========================================================

    def classify(self, score_report):
        """
        Classifies the overall project score.

        Parameters
        ----------
        score_report : dict
            Output from OverallScoreCalculator.

        Returns
        -------
        dict
            Grade assessment.
        """

        score = score_report["overall_score"]

        if score >= 90:

            grade = "EXCELLENT"

            rationale = [
                "The project demonstrates outstanding overall quality."
            ]

        elif score >= 80:

            grade = "VERY GOOD"

            rationale = [
                "The project is production-ready with only minor improvements recommended."
            ]

        elif score >= 70:

            grade = "GOOD"

            rationale = [
                "The project is generally well implemented but has several areas for improvement."
            ]

        elif score >= 60:

            grade = "FAIR"

            rationale = [
                "The project is functional but requires noticeable improvements before production deployment."
            ]

        elif score >= 40:

            grade = "POOR"

            rationale = [
                "The project contains significant issues that should be addressed."
            ]

        else:

            grade = "CRITICAL"

            rationale = [
                "The project is not ready for deployment and requires major improvements."
            ]

        return {

            "grade": grade,

            "grade_range": self._grade_range(grade),

            "deployment_recommendation":
                self._deployment_recommendation(grade),

            "rationale": rationale,

            # Entire score calculation
            "score_report": score_report,

        }

    # ==========================================================
    # Grade Range
    # ==========================================================

    def _grade_range(self, grade):
        """
        Returns the score range for a grade.
        """

        ranges = {

            "EXCELLENT": "90-100",

            "VERY GOOD": "80-89",

            "GOOD": "70-79",

            "FAIR": "60-69",

            "POOR": "40-59",

            "CRITICAL": "0-39",

        }

        return ranges[grade]

    # ==========================================================
    # Deployment Recommendation
    # ==========================================================

    def _deployment_recommendation(self, grade):
        """
        Returns deployment guidance.
        """

        recommendations = {

            "EXCELLENT":
                "Ready for production deployment.",

            "VERY GOOD":
                "Ready for deployment after minor improvements.",

            "GOOD":
                "Deployment is acceptable after recommended improvements.",

            "FAIR":
                "Deployment is not recommended until important issues are resolved.",

            "POOR":
                "Major improvements are required before deployment.",

            "CRITICAL":
                "Deployment should not proceed until critical issues are fixed.",

        }

        return recommendations[grade]