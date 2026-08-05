from app.recommendations.recommendation import Recommendation


class RecommendationParser:

    def parse(self, data):

        recommendations = []

        for item in data.get(
            "recommendations",
            []
        ):

            recommendations.append(

                Recommendation(

                    title=item.get("title", ""),

                    description=item.get(
                        "description",
                        ""
                    ),

                    priority=item.get(
                        "priority",
                        ""
                    ),

                    category=item.get(
                        "category",
                        ""
                    ),

                    impact=item.get(
                        "impact",
                        ""
                    ),

                    code_location=item.get(
                        "code_location",
                        ""
                    ),

                    suggested_fix=item.get(
                        "suggested_fix",
                        ""
                    ),

                    reasoning=item.get(
                        "reasoning",
                        ""
                    )

                )

            )

        return recommendations