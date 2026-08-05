from dataclasses import dataclass, field


@dataclass
class ClassModel:
    """
    Represents a class extracted from any programming language.
    """

    name: str

    language: str

    methods: list = field(default_factory=list)

    attributes: list = field(default_factory=list)

    base_classes: list = field(default_factory=list)

    decorators: list = field(default_factory=list)

    start_line: int = 0

    end_line: int = 0

    source_code: str = ""

    business_role: str = ""

    matched_requirements: list = field(default_factory=list)

    confidence: float = 0.0