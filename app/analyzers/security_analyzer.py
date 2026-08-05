from app.models.finding import Finding
from app.security.security_scanner import SecurityScanner


class SecurityAnalyzer:
    """
    Purpose:
        Detect security vulnerabilities using Bandit.

    Responsibilities:
        - Execute the SecurityScanner.
        - Convert Bandit findings into standardized Finding objects.
        - Return a list of security findings.
    """

    def __init__(self):

        self.scanner = SecurityScanner()

    def analyze(self, graph):

        findings = []

        for filename, file in graph.files.items():

            if file.get("extension") != ".py":
                continue

            issues = self.scanner.scan(
                file.get("content", "")
            )

            for issue in issues:

                findings.append(

                    Finding(

                        rule=issue.get("test_id", "UNKNOWN"),

                        severity=issue.get(
                            "issue_severity",
                            "INFO"
                        ),

                        file=filename,

                        line=issue.get("line_number"),

                        message=issue.get(
                            "issue_text",
                            "Security issue detected."
                        ),

                        evidence={

                            "test_name":
                                issue.get("test_name"),

                            "confidence":
                                issue.get("issue_confidence"),

                            "cwe":
                                issue.get(
                                    "issue_cwe",
                                    {}
                                ).get("id"),

                            "more_info":
                                issue.get("more_info")
                        }

                    ).to_dict()

                )

        return findings