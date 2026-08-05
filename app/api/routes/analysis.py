from fastapi import APIRouter

from app.api.models.request_models import AnalyzeRequest
from app.api.models.response_models import AnalyzeResponse
from app.api.services.analysis_service import AnalysisService

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"],
)

service = AnalysisService()


@router.post(
    "",
    response_model=AnalyzeResponse,
    summary="Analyze Software Project",
    description="""
Analyzes a software project using the AISES analysis engine.

The analysis pipeline performs:

- Requirement Assessment
- Security Assessment
- Performance Assessment
- Best Practice Assessment
- AI Evaluation
- Overall Assessment
- Recommendation Generation

A comprehensive assessment report is returned in the requested export format.
""",
    response_description="Analysis completed successfully.",
)
def analyze(request: AnalyzeRequest):

    report = service.analyze(
        project_path=request.project_path,
        export_format=request.export_format,
        include_ai_evaluation=request.include_ai_evaluation,
    )

    return AnalyzeResponse(
        success=True,
        message="Project analyzed successfully.",
        report=report,
    )