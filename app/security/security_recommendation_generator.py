#component4 
class SecurityRecommendationGenerator:
    """
    Generates developer-friendly recommendations for
    detected security issues.
    """

    RECOMMENDATIONS = {

        "B105": {
            "title": "Hardcoded Password",

            "priority": "MEDIUM",

            "recommendation":
                "Avoid hardcoding passwords in source code. "
                "Store credentials in environment variables, "
                "configuration files, or a dedicated secrets manager."
        },

        "B307": {
            "title": "Use of eval()",

            "priority": "HIGH",

            "recommendation":
                "Avoid using eval() because it can execute "
                "untrusted input. Use ast.literal_eval() or "
                "implement explicit input parsing."
        }

    }

    DEFAULT = {

        "title": "Security Improvement",

        "priority": "LOW",

        "recommendation":
            "Review this security finding and follow secure "
            "coding practices."
    }

    def generate(self, security_report):

        recommendations = []

        seen = set()

        for finding in security_report["findings"]:

            rule = finding["rule"]

            if rule in seen:
                continue

            seen.add(rule)

            details = self.RECOMMENDATIONS.get(
                rule,
                self.DEFAULT
            )

            recommendations.append(
                {
                    "rule": rule,
                    "title": details["title"],
                    "priority": details["priority"],
                    "recommendation": details["recommendation"]
                }
            )

        return recommendations