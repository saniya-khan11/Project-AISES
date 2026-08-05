from dataclasses import dataclass, field

@dataclass
class AIResponse:

    success: bool = False

    raw_response: str = ""

    parsed_data: dict = field(default_factory=dict)

    confidence: float = 0.0

    model: str = ""

    execution_time: float = 0.0

    errors: list = field(default_factory=list)

    warnings: list = field(default_factory=list)