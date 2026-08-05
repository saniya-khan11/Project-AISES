class RecommendationSummarizer:
    """
    Generates a summary for the recommendation report.

    Responsibilities
    ----------------
    - Generate recommendation statistics
    - Group recommendations by category
    - Produce a human-readable summary
    """

    CATEGORY_ORDER = [

        "Requirement",

        "Security",

        "Performance",

        "Best Practice",

        "AI",

    ]

    # ==========================================================
    # Summarize
    # ==========================================================

    def summarize(self, recommendation_report):
        """
        Generates a recommendation summary.

        Parameters
        ----------
        recommendation_report : dict

        Returns
        -------
        dict
        """

        recommendations = recommendation_report["recommendations"]

        summary = recommendation_report["summary"]

        category_summary = self._category_summary(
            recommendations
        )

        narrative = self._generate_narrative(
            summary
        )

        return {

            "summary": summary,

            "priority_order":
                recommendation_report["priority_order"],

            "category_order":
                self.CATEGORY_ORDER,

            "category_summary":
                category_summary,

            "narrative":
                narrative,

            "recommendations":
                recommendations,

        }

    # ==========================================================
    # Category Summary
    # ==========================================================

    def _category_summary(
        self,
        recommendations,
    ):
        """
        Counts recommendations by category.
        """

        categories = {}

        for recommendation in recommendations:

            category = recommendation.get(
                "category",
                "Unknown",
            )

            categories[category] = (
                categories.get(category, 0) + 1
            )

        ordered_categories = {}

        for category in self.CATEGORY_ORDER:

            if category in categories:

                ordered_categories[category] = categories[
                    category
                ]

        for category in categories:

            if category not in ordered_categories:

                ordered_categories[category] = categories[
                    category
                ]

        return ordered_categories

    # ==========================================================
    # Narrative
    # ==========================================================

    def _generate_narrative(
        self,
        summary,
    ):
        """
        Generates a human-readable summary.
        """

        total = summary["total_recommendations"]

        if total == 0:

            return (
                "No recommendations were generated. "
                "The project appears ready for deployment."
            )

        return (

            f"{total} recommendation(s) identified. "

            f"{summary['critical']} critical, "

            f"{summary['high']} high, "

            f"{summary['medium']} medium, "

            f"{summary['low']} low, "

            f"and {summary['info']} informational recommendation(s)."

        )