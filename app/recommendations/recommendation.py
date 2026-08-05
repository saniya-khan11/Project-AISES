from dataclasses import dataclass


@dataclass
class Recommendation:

    title: str

    description: str

    priority: str

    category: str

    impact: str

    code_location: str = ""

    suggested_fix: str = ""

    reasoning: str = ""