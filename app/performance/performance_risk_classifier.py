class PerformanceRiskClassifier:
    """
    Classifies the overall performance quality of the project.

    Responsibilities
    ----------------
    - Determine performance risk.
    - Produce an explainable rationale.
    """

    def classify(self, metrics):

        score = metrics["performance_score"]

        summary = metrics["summary"]

        distribution = metrics["distribution"]

        rationale = []

        # -------------------------------------------------
        # Excellent
        # -------------------------------------------------

        if score >= 90:

            risk = "EXCELLENT"

            rationale.append(
                "No significant performance issues detected."
            )

        # -------------------------------------------------
        # Good
        # -------------------------------------------------

        elif score >= 75:

            risk = "GOOD"

            rationale.append(
                "Minor performance improvements are recommended."
            )

        # -------------------------------------------------
        # Fair
        # -------------------------------------------------

        elif score >= 50:

            risk = "FAIR"

            rationale.append(
                "Several performance issues should be addressed."
            )

        # -------------------------------------------------
        # Poor
        # -------------------------------------------------

        else:

            risk = "POOR"

            rationale.append(
                "Performance optimization is strongly recommended."
            )

        return {

            "risk": risk,

            "score": score,

            "summary": summary,

            "distribution": distribution,

            "rationale": rationale
        }