from dataclasses import dataclass, field
from typing import List


@dataclass
class AcceptanceCriteria:

    ac_id: str

    requirement_id: str

    requirement_title: str

    description: str

    priority: str

    inputs: List[str] = field(default_factory=list)

    expected_outputs: List[str] = field(default_factory=list)

    preconditions: List[str] = field(default_factory=list)

    postconditions: List[str] = field(default_factory=list)

    keywords: List[str] = field(default_factory=list)


@dataclass
class RequirementDocument:

    project_name: str

    project_description: str

    acceptance_criteria: List[AcceptanceCriteria]