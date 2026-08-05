#component 8.3
class SecurityRiskClassifier:
    """
    Determines the overall security risk level based on
    security severity statistics.

    Responsibilities
    ----------------
    - Classify overall project security risk.
    - Produce an explainable rationale.
    - Generate a normalized security score.
    """

    def classify(self, severity_report):

        summary = severity_report["summary"]
        distribution = severity_report["distribution"]

        critical = summary["critical"]
        high = summary["high"]
        medium = summary["medium"]
        low = summary["low"]

        rationale = []

        # -------------------------------------------------
        # Critical Risk
        # -------------------------------------------------

        if critical > 0:

            risk = "CRITICAL"
            score = 100

            rationale.append(
                f"{critical} critical vulnerability(ies) detected."
            )

        # -------------------------------------------------
        # High Risk
        # -------------------------------------------------

        elif high >= 2:

            risk = "HIGH"
            score = 75

            rationale.append(
                f"{high} high-severity vulnerabilities detected."
            )

        # -------------------------------------------------
        # Medium Risk
        # -------------------------------------------------

        elif high == 1:

            risk = "MEDIUM"
            score = 50

            rationale.append(
                "One high-severity vulnerability detected."
            )

        elif medium >= 3:

            risk = "MEDIUM"
            score = 50

            rationale.append(
                f"{medium} medium-severity vulnerabilities detected."
            )

        # -------------------------------------------------
        # Low Risk
        # -------------------------------------------------

        elif medium > 0:

            risk = "LOW"
            score = 25

            rationale.append(
                f"{medium} medium-severity vulnerability(ies) detected."
            )

        elif low > 0:

            risk = "LOW"
            score = 10

            rationale.append(
                f"{low} low-severity vulnerability(ies) detected."
            )

        # -------------------------------------------------
        # Secure
        # -------------------------------------------------

        else:

            risk = "SECURE"
            score = 0

            rationale.append(
                "No security vulnerabilities detected."
            )

        return {
            "risk": risk,
            "score": score,
            "summary": summary,
            "distribution": distribution,
            "rationale": rationale
        }