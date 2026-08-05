class PerformanceRecommendationGenerator:
    """
    Generates recommendations for improving code performance
    and maintainability.
    """

    RECOMMENDATIONS = {

        "HIGH_CYCLOMATIC_COMPLEXITY": {

            "title": "Reduce Cyclomatic Complexity",

            "priority": "HIGH",

            "recommendation":
                "Break the function into smaller functions, "
                "reduce nested branching, and simplify decision logic."
        },

        "LOW_MAINTAINABILITY": {

            "title": "Improve Maintainability",

            "priority": "MEDIUM",

            "recommendation":
                "Refactor large or complex code into smaller, "
                "well-structured and reusable components."
        }

    }

    DEFAULT = {

        "title": "Performance Improvement",

        "priority": "LOW",

        "recommendation":
            "Review this performance issue and apply appropriate "
            "code optimization techniques."
    }

    def generate(self, performance_report):

        recommendations = []

        seen = set()

        for finding in performance_report["findings"]:

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