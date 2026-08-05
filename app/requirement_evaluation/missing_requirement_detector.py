from app.requirement_evaluation.requirement_assessment import (
    RequirementAssessment,
)


class MissingRequirementDetector:
    """
    Determines whether a requirement
    is implemented, partially implemented,
    or missing.
    """

    def evaluate(
        self,
        requirement,
        capability,
    ):

        assessment = RequirementAssessment(

            requirement_id=requirement.id,

            requirement=requirement.description,

            status="Missing",

            confidence=0.0,
        )

        req = requirement.description.lower()

        capability_name = capability.primary_capability.lower()

        if any(word in req for word in capability_name.split()):

            assessment.status = "Implemented"

            assessment.confidence = capability.confidence

            assessment.matched_capability = (
                capability.primary_capability
            )

            assessment.evidence.extend(
                capability.sub_capabilities
            )

        else:

            assessment.status = "Missing"

            assessment.confidence = 0.10

            assessment.recommendation = (
                "Required capability not found in implementation."
            )

        assessment.ai_reasoning = (
            "Rule-based requirement evaluation."
        )

        return assessment