from typing import Optional

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """
    Request model for project analysis.
    """

    project_path: str = Field(
        ...,
        description="Path to the project directory.",
        examples=["examples/sample_project"],
    )

    export_format: str = Field(
        default="json",
        description="Desired report format.",
        examples=["json", "text", "markdown"],
    )

    include_ai_evaluation: bool = Field(
        default=True,
        description="Enable AI evaluation.",
    )

    save_report: bool = Field(
        default=False,
        description="Save the generated report to disk.",
    )

    output_directory: Optional[str] = Field(
        default=None,
        description="Directory where the report should be saved.",
    )