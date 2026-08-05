#component 8.5
class SecurityAssessment:
    """
    Builds the complete security assessment.

    Responsibilities
    ----------------
    - Assemble security findings.
    - Assemble severity metrics.
    - Assemble overall risk.
    - Assemble recommendations.
    """

    def build(
        self,
        security_report,
        severity_report,
        risk_report,
        recommendations
    ):

        return {

            "summary": {

                "total_findings":
                    severity_report["summary"]["total_findings"],

                "risk":
                    risk_report["risk"],

                "security_score":
                    risk_report["score"]

            },

            "severity":
                severity_report,

            "risk":
                risk_report,

            "findings":
                security_report["findings"],

            "recommendations":
                recommendations
        }