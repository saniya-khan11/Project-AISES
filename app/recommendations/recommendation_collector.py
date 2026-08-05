class RecommendationCollector:
    """
    Collects recommendations from all assessment modules.

    Responsibilities
    ----------------
    - Requirement recommendations
    - Security recommendations
    - Performance recommendations
    - Best-practice recommendations
    - AI suggestions

    Does NOT:
    - Prioritize
    - Deduplicate
    - Summarize
    """

    # ==========================================================
    # Collect
    # ==========================================================

    def collect(
        self,
        requirement_assessment,
        security_assessment,
        performance_assessment,
        best_practice_assessment,
        ai_evaluation,
    ):
        """
        Collects recommendations from all assessment modules.

        Returns
        -------
        list
        """

        recommendations = []

        recommendations.extend(
            self._collect_requirement(requirement_assessment)
        )

        recommendations.extend(
            self._collect_security(security_assessment)
        )

        recommendations.extend(
            self._collect_performance(performance_assessment)
        )

        recommendations.extend(
            self._collect_best_practice(best_practice_assessment)
        )

        recommendations.extend(
            self._collect_ai(ai_evaluation)
        )

        return recommendations

    # ==========================================================
    # Helper
    # ==========================================================

    def _create_recommendation(
        self,
        recommendation_id,
        source,
        priority,
        category,
        title,
        recommendation,
    ):
        """
        Creates a standardized recommendation object.
        """

        return {

            "id": recommendation_id,

            "source": source,

            "priority": priority,

            "category": category,

            "title": title,

            "recommendation": recommendation,

        }

    # ==========================================================
    # Requirement
    # ==========================================================

    def _collect_requirement(self, assessment):

        results = []

        for index, finding in enumerate(
            assessment.get("recommendations", []),
            start=1,
        ):

            results.append(

                self._create_recommendation(

                    recommendation_id=f"REQ-{index:03}",

                    source="requirement",

                    priority=finding.get(
                        "priority",
                        "MEDIUM",
                    ),

                    category="Requirement",

                    title=finding.get(
                        "title",
                        "",
                    ),

                    recommendation=finding.get(
                        "recommendation",
                        "",
                    ),

                )

            )

        return results

    # ==========================================================
    # Security
    # ==========================================================

    def _collect_security(self, assessment):

        results = []

        for index, finding in enumerate(
            assessment.get("recommendations", []),
            start=1,
        ):

            results.append(

                self._create_recommendation(

                    recommendation_id=f"SEC-{index:03}",

                    source="security",

                    priority=finding.get(
                        "priority",
                        "MEDIUM",
                    ),

                    category="Security",

                    title=finding.get(
                        "title",
                        "",
                    ),

                    recommendation=finding.get(
                        "recommendation",
                        "",
                    ),

                )

            )

        return results

    # ==========================================================
    # Performance
    # ==========================================================

    def _collect_performance(self, assessment):

        results = []

        for index, finding in enumerate(
            assessment.get("recommendations", []),
            start=1,
        ):

            results.append(

                self._create_recommendation(

                    recommendation_id=f"PER-{index:03}",

                    source="performance",

                    priority=finding.get(
                        "priority",
                        "MEDIUM",
                    ),

                    category="Performance",

                    title=finding.get(
                        "title",
                        "",
                    ),

                    recommendation=finding.get(
                        "recommendation",
                        "",
                    ),

                )

            )

        return results

    # ==========================================================
    # Best Practice
    # ==========================================================

    def _collect_best_practice(self, assessment):

        results = []

        for index, finding in enumerate(
            assessment.get("recommendations", []),
            start=1,
        ):

            results.append(

                self._create_recommendation(

                    recommendation_id=f"BP-{index:03}",

                    source="best_practice",

                    priority=finding.get(
                        "priority",
                        "MEDIUM",
                    ),

                    category="Best Practice",

                    title=finding.get(
                        "title",
                        "",
                    ),

                    recommendation=finding.get(
                        "recommendation",
                        "",
                    ),

                )

            )

        return results

    # ==========================================================
    # AI Suggestions
    # ==========================================================

    def _collect_ai(self, ai_report):

        results = []

        for index, suggestion in enumerate(
            ai_report.get("suggestions", []),
            start=1,
        ):

            results.append(

                self._create_recommendation(

                    recommendation_id=f"AI-{index:03}",

                    source="ai",

                    priority="MEDIUM",

                    category="AI",

                    title="AI Suggestion",

                    recommendation=suggestion,

                )

            )

        return results