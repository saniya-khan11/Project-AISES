from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Finding:
    """
    Represents a single analysis finding produced by any analyzer.
    """

    rule: str
    severity: str
    file: str
    message: str
    line: int | None = None
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "rule": self.rule,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "message": self.message,
            "evidence": self.evidence,
        }