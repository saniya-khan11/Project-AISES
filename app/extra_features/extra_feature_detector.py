from app.extra_features.extra_feature import ExtraFeature


class ExtraFeatureDetector:
    """
    Detects business capabilities that are
    present in code but absent in the SRS.
    """

    def detect(self, requirements, capabilities):

        # Convert all requirement descriptions to lowercase
        requirement_text = " ".join(
            r.description.lower() for r in requirements
        )

        extras = []

        for capability in capabilities:

            for sub in capability.sub_capabilities:

                # Very simple prototype rule
                if not any(word in requirement_text
                           for word in sub.lower().split()):

                    extras.append(

                        ExtraFeature(

                            feature=sub,

                            function_name=capability.function_name,

                            evidence=[

                                capability.primary_capability,

                                sub

                            ],

                            confidence=0.85,

                            ai_reasoning=(
                                "Capability not found in SRS."
                            ),

                            recommendation=(
                                "Remove feature or update SRS."
                            )

                        )

                    )

        return extras