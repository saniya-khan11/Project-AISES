class PerformanceMetricsCalculator:
    """
    Calculates performance metrics from collected evidence.

    Responsibilities
    ----------------
    - Count findings by severity.
    - Calculate severity distribution.
    - Compute a performance score.
    """

    def calculate(self, performance_report):

        findings = performance_report["findings"]

        summary = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0,
            "total_findings": len(findings)
        }

        # ---------------------------------------------
        # Count severities
        # ---------------------------------------------

        for finding in findings:

            severity = finding["severity"].upper()

            if severity == "CRITICAL":
                summary["critical"] += 1

            elif severity in ("HIGH", "ERROR"):
                summary["high"] += 1

            elif severity in ("MEDIUM", "WARNING"):
                summary["medium"] += 1

            elif severity == "LOW":
                summary["low"] += 1

            else:
                summary["info"] += 1

        # ---------------------------------------------
        # Distribution
        # ---------------------------------------------

        total = max(summary["total_findings"], 1)

        distribution = {}

        for level in [
            "critical",
            "high",
            "medium",
            "low",
            "info"
        ]:

            distribution[level.upper()] = {
                "count": summary[level],
                "percentage": round(
                    (summary[level] / total) * 100,
                    2
                )
            }

        # ---------------------------------------------
        # Performance Score
        # ---------------------------------------------

        score = 100

        score -= summary["critical"] * 40
        score -= summary["high"] * 20
        score -= summary["medium"] * 10
        score -= summary["low"] * 5

        score = max(score, 0)

        return {

            "summary": summary,

            "distribution": distribution,

            "performance_score": score
        }