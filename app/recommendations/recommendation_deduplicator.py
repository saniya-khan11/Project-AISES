class RecommendationDeduplicator:
    """
    Removes duplicate recommendations while preserving priority order.
    """

    PRIORITY_ORDER = {
        "CRITICAL": 5,
        "HIGH": 4,
        "MEDIUM": 3,
        "LOW": 2,
        "INFO": 1,
    }

    # ==========================================================
    # Deduplicate
    # ==========================================================

    def deduplicate(self, prioritized_report):
        """
        Removes duplicate recommendations.

        Parameters
        ----------
        prioritized_report : dict

        Returns
        -------
        dict
        """

        recommendations = prioritized_report["recommendations"]

        seen = set()
        unique = []

        for recommendation in recommendations:

            key = recommendation.get(
                "recommendation",
                "",
            ).strip().lower()

            if key in seen:
                continue

            seen.add(key)
            unique.append(recommendation)

        # ------------------------------------------------------
        # Ensure correct priority ordering
        # ------------------------------------------------------

        unique.sort(
            key=lambda recommendation: (
                self.PRIORITY_ORDER.get(
                    recommendation.get(
                        "priority",
                        "MEDIUM",
                    ).upper(),
                    3,
                ),
                recommendation.get("category", ""),
                recommendation.get("title", ""),
            ),
            reverse=True,
        )

        summary = {

            "total_recommendations": len(unique),

            "duplicates_removed":
                len(recommendations) - len(unique),

            "critical": self._count(unique, "CRITICAL"),

            "high": self._count(unique, "HIGH"),

            "medium": self._count(unique, "MEDIUM"),

            "low": self._count(unique, "LOW"),

            "info": self._count(unique, "INFO"),

        }

        return {

            "summary": summary,

            "priority_order":
                prioritized_report["priority_order"],

            "recommendations": unique,

        }

    # ==========================================================
    # Count Helper
    # ==========================================================

    def _count(
        self,
        recommendations,
        priority,
    ):

        return sum(

            recommendation.get(
                "priority",
                "",
            ).upper() == priority

            for recommendation in recommendations

        )