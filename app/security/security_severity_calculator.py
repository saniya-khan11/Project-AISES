from collections import Counter


class SecuritySeverityCalculator:
    """
    Calculates severity statistics for security findings.

    Responsibilities
    ----------------
    - Count findings by severity.
    - Calculate severity percentages.
    - Produce structured statistics for the
      Security Risk Classifier.
    """

    SEVERITIES = [
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW",
        "INFO"
    ]

    def calculate(self, security_report):

        findings = security_report["findings"]

        counter = Counter()

        for finding in findings:

            severity = finding["severity"].upper()

            counter[severity] += 1

        total = len(findings)

        distribution = {}

        for severity in self.SEVERITIES:

            count = counter.get(severity, 0)

            percentage = (
                round((count / total) * 100, 2)
                if total > 0
                else 0.0
            )

            distribution[severity] = {
                "count": count,
                "percentage": percentage
            }

        summary = {
            "total_findings": total,
            "critical": counter.get("CRITICAL", 0),
            "high": counter.get("HIGH", 0),
            "medium": counter.get("MEDIUM", 0),
            "low": counter.get("LOW", 0),
            "info": counter.get("INFO", 0)
        }

        return {
            "summary": summary,
            "distribution": distribution
        }