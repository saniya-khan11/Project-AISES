#component 8.1
class SecurityEvidenceAnalyzer:
    """
    Extracts only security-related findings from the
    complete evidence repository.

    Responsibilities
    ----------------
    - Filter security findings.
    - Build security summary statistics.
    - Prepare structured security evidence for later modules.
    """

    def analyze(self, evidence):

        security_findings = []

        for finding in evidence.findings:

            # ----------------------------------------
            # Bandit findings
            # ----------------------------------------

            if finding["rule"].startswith("B"):

                security_findings.append(finding)

        summary = {
            "total_security_findings": len(security_findings),

            "files_affected": len(
                {
                    finding["file"]
                    for finding in security_findings
                }
            ),

            "rules_detected": sorted(
                {
                    finding["rule"]
                    for finding in security_findings
                }
            )
        }

        return {
            "summary": summary,
            "findings": security_findings
        }