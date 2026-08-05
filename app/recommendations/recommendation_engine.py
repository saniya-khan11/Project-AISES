from app.recommendations.recommendation_collector import (
    RecommendationCollector,
)

from app.recommendations.recommendation_deduplicator import (
    RecommendationDeduplicator,
)

from app.recommendations.recommendation_prioritizer import (
    RecommendationPrioritizer,
)

from app.recommendations.recommendation_summarizer import (
    RecommendationSummarizer,
)

from app.recommendations.ai_recommendation_generator import (
    AIRecommendationGenerator,
)


class RecommendationEngine:
    """
    Recommendation Engine.

    Responsibilities
    ----------------
    - Collect rule-based recommendations
    - Generate AI recommendations
    - Merge recommendations
    - Prioritize recommendations
    - Remove duplicate recommendations
    - Generate recommendation summary

    Acts as the public API for the recommendation subsystem.
    """

    def __init__(self):

        self.collector = RecommendationCollector()

        self.ai_generator = AIRecommendationGenerator()

        self.prioritizer = RecommendationPrioritizer()

        self.deduplicator = RecommendationDeduplicator()

        self.summarizer = RecommendationSummarizer()

    # ==========================================================
    # Generate Recommendations
    # ==========================================================

    def generate(
        self,
        requirement_assessment,
        security_assessment,
        performance_assessment,
        best_practice_assessment,
        ai_evaluation,
    ):
        """
        Executes the complete recommendation pipeline.
        """

        # ------------------------------------------------------
        # Step 1 : Collect Rule-Based Recommendations
        # ------------------------------------------------------

        collected = self.collector.collect(
            requirement_assessment,
            security_assessment,
            performance_assessment,
            best_practice_assessment,
            ai_evaluation,
        )

        # ------------------------------------------------------
        # Step 2 : Generate AI Recommendations
        # ------------------------------------------------------

        ai_recommendations = self.ai_generator.generate(
            {
                "requirement_assessment": requirement_assessment,
                "security_assessment": security_assessment,
                "performance_assessment": performance_assessment,
                "best_practice_assessment": best_practice_assessment,
                "ai_evaluation": ai_evaluation,
            }
        )

        # Merge AI recommendations with collected recommendations
        if ai_recommendations:
            collected.extend(ai_recommendations)

        # ------------------------------------------------------
        # Step 3 : Prioritize
        # ------------------------------------------------------

        prioritized = self.prioritizer.prioritize(
            collected
        )

        # ------------------------------------------------------
        # Step 4 : Remove Duplicates
        # ------------------------------------------------------

        deduplicated = self.deduplicator.deduplicate(
            prioritized
        )

        # ------------------------------------------------------
        # Step 5 : Generate Summary
        # ------------------------------------------------------

        summary = self.summarizer.summarize(
            deduplicated
        )

        # ------------------------------------------------------
        # Return Final Report
        # ------------------------------------------------------

        return {

            "summary": summary["summary"],

            "priority_order": summary["priority_order"],

            "category_order": summary["category_order"],

            "category_summary": summary["category_summary"],

            "narrative": summary["narrative"],

            "recommendations": summary["recommendations"],

        }