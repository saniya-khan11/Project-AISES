from app.engine.analysis_engine import AnalysisEngine


class AnalysisService:
    """
    Executes the AISES analysis pipeline.
    """

    def __init__(self):

        self.engine = AnalysisEngine()

    def analyze(
        self,
        project_path: str,
        export_format: str = "json",
        include_ai_evaluation: bool = True,
    ):

        return self.engine.run(
            project_path=project_path,
            export_format=export_format,
            include_ai_evaluation=include_ai_evaluation,
        )