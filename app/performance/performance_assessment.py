class PerformanceAssessment:
    """
    Builds the complete performance assessment.

    Responsibilities
    ----------------
    - Assemble performance findings.
    - Assemble performance metrics.
    - Assemble overall performance risk.
    - Assemble optimization recommendations.
    """

    def build(
        self,
        performance_report,
        metrics_report,
        risk_report,
        recommendations,
    ):

        return {

            "summary": {

                "total_findings":
                    metrics_report["summary"]["total_findings"],

                "performance_score":
                    metrics_report["performance_score"],

                "risk":
                    risk_report["risk"]

            },

            "metrics":
                metrics_report,

            "risk":
                risk_report,

            "findings":
                performance_report["findings"],

            "recommendations":
                recommendations
        }