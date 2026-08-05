class RecommendationPrioritizer:
    """
    Sorts recommendations based on priority.

    Priority Order
    --------------
    CRITICAL
    HIGH
    MEDIUM
    LOW
    INFO
    """

    PRIORITY_ORDER = {

        "CRITICAL": 5,

        "HIGH": 4,

        "MEDIUM": 3,

        "LOW": 2,

        "INFO": 1,

    }

    # ==========================================================
    # Prioritize
    # ==========================================================

    def prioritize(self, recommendations):
        """
        Sort recommendations by priority.

        Parameters
        ----------
        recommendations : list

        Returns
        -------
        dict
        """

        prioritized = sorted(

            recommendations,

            key=lambda recommendation: (

                self.PRIORITY_ORDER.get(

                    recommendation.get(
                        "priority",
                        "MEDIUM",
                    ).upper(),

                    3,

                ),

                recommendation.get(
                    "category",
                    "",
                ),

                recommendation.get(
                    "title",
                    "",
                ),

            ),

            reverse=True,

        )

        summary = {

            "total_recommendations": len(prioritized),

            "critical": self._count(
                prioritized,
                "CRITICAL",
            ),

            "high": self._count(
                prioritized,
                "HIGH",
            ),

            "medium": self._count(
                prioritized,
                "MEDIUM",
            ),

            "low": self._count(
                prioritized,
                "LOW",
            ),

            "info": self._count(
                prioritized,
                "INFO",
            ),

        }

        return {

            "summary": summary,

            "priority_order": [

                "CRITICAL",

                "HIGH",

                "MEDIUM",

                "LOW",

                "INFO",

            ],

            "recommendations": prioritized,

        }

    # ==========================================================
    # Count Helper
    # ==========================================================

    def _count(
        self,
        recommendations,
        priority,
    ):
        """
        Counts recommendations for the specified priority.
        """

        return sum(

            recommendation.get(
                "priority",
                "",
            ).upper() == priority

            for recommendation in recommendations

        )