from typing import Any

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str


class AnalyzeResponse(BaseModel):
    """
    Response returned after project analysis.
    """

    success: bool

    message: str

    report: Any


class ErrorResponse(BaseModel):
    """
    Standard API error response.
    """

    success: bool

    error: str

    details: str | None = None