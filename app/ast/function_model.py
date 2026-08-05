from dataclasses import dataclass, field


@dataclass
class FunctionModel:
    """
    Represents a function extracted from any programming language.

    This object will gradually be enriched by later AISES modules.
    """

    # ==========================================================
    # Basic Information
    # ==========================================================

    name: str

    language: str

    parameters: list = field(default_factory=list)

    return_type: str = "Unknown"

    start_line: int = 0

    end_line: int = 0

    source_code: str = ""

    # ==========================================================
    # Code Intelligence
    # ==========================================================

    called_functions: list = field(default_factory=list)

    local_variables: list = field(default_factory=list)

    global_variables: list = field(default_factory=list)

    imports: list = field(default_factory=list)

    decorators: list = field(default_factory=list)

    exceptions: list = field(default_factory=list)

    comments: list = field(default_factory=list)

    # ==========================================================
    # API Information
    # ==========================================================

    api_endpoint: str = ""

    http_method: str = ""

    # ==========================================================
    # Requirement Matching
    # ==========================================================

    business_intent: str = ""

    matched_requirements: list = field(default_factory=list)

    confidence: float = 0.0

    # ==========================================================
    # AI Analysis
    # ==========================================================

    semantic_embedding: list = field(default_factory=list)

    ai_summary: str = ""

    recommendation: str = ""


    api_endpoint: str = ""

    http_method: str = ""

    database_tables: list = field(default_factory=list)

    database_operations: list = field(default_factory=list)