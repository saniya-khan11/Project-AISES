from dataclasses import dataclass, field


@dataclass
class ExtraFeature:

    feature: str

    function_name: str

    evidence: list = field(default_factory=list)

    confidence: float = 0.0

    ai_reasoning: str = ""

    recommendation: str = ""