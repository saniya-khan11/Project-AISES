class PerformanceEvidenceAnalyzer:
    """
    Collects performance-related evidence from static analysis.

    Responsibilities
    ----------------
    - Collect complexity findings.
    - Collect maintainability findings.
    - Produce summary statistics.
    """

    def analyze(self, evidence):

        performance_findings = []

        # -------------------------------------------------
        # Complexity Findings
        # -------------------------------------------------

        for finding in evidence.findings:

            if finding["rule"] == "HIGH_CYCLOMATIC_COMPLEXITY":

                performance_findings.append(finding)

        # -------------------------------------------------
        # Maintainability Findings
        # -------------------------------------------------

        for finding in evidence.findings:

            if finding["rule"].startswith("LOW_MAINTAINABILITY"):

                performance_findings.append(finding)

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        files = {
            finding["file"]
            for finding in performance_findings
        }

        return {

            "summary": {

                "total_performance_findings":
                    len(performance_findings),

                "files_affected":
                    len(files),

                "finding_types":
                    sorted(
                        {
                            finding["rule"]
                            for finding in performance_findings
                        }
                    )

            },

            "findings":
                performance_findings
        }