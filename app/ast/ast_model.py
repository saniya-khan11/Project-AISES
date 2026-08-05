from dataclasses import dataclass, field


@dataclass
class ASTNode:
    """
    Common AST node used across all languages.
    """

    node_type: str

    name: str = ""

    start_line: int = 0

    end_line: int = 0

    children: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)