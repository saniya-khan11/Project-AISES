from dataclasses import dataclass, field


@dataclass
class RequirementAssessment:

    requirement_id: str

    requirement: str

    status: str

    confidence: float

    matched_capability: str = ""

    evidence: list = field(default_factory=list)

    missing_sub_capabilities: list = field(default_factory=list)

    ai_reasoning: str = ""

    recommendation: str = ""