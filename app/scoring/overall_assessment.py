#component 12.4

from app.scoring.overall_score_calculator import (
    OverallScoreCalculator,
)
from app.scoring.score_breakdown_generator import (
    ScoreBreakdownGenerator,
)
from app.scoring.score_grade_classifier import (
    ScoreGradeClassifier,
)


class OverallAssessment:
    """
    Overall Scoring Assessment.

    Responsibilities
    ----------------
    - Calculate overall score.
    - Classify project grade.
    - Generate score breakdown.
    - Return the complete scoring assessment.
    """

    def __init__(self):

        self.score_calculator = OverallScoreCalculator()

        self.grade_classifier = ScoreGradeClassifier()

        self.breakdown_generator = ScoreBreakdownGenerator()

    # ==========================================================
    # Assess
    # ==========================================================

    def assess(
        self,
        requirement_assessment,
        security_assessment,
        performance_assessment,
        best_practice_assessment,
    ):
        """
        Executes the complete scoring pipeline.

        Parameters
        ----------
        requirement_assessment : dict

        security_assessment : dict

        performance_assessment : dict

        best_practice_assessment : dict

        Returns
        -------
        dict
        """

        # ------------------------------------------------------
        # Step 1: Calculate Score
        # ------------------------------------------------------

        score_report = self.score_calculator.calculate(
            requirement_assessment,
            security_assessment,
            performance_assessment,
            best_practice_assessment,
        )

        # ------------------------------------------------------
        # Step 2: Grade Classification
        # ------------------------------------------------------

        grade_report = self.grade_classifier.classify(
            score_report
        )

        # ------------------------------------------------------
        # Step 3: Breakdown
        # ------------------------------------------------------

        breakdown_report = self.breakdown_generator.generate(
            grade_report
        )

        # ------------------------------------------------------
        # Return Complete Assessment
        # ------------------------------------------------------

        return {

        "summary": {

        "overall_score": score_report["overall_score"],

        "max_score": score_report["max_score"],

        "grade": grade_report["grade"],

        "deployment_recommendation":
            grade_report["deployment_recommendation"]

        },

    "score": score_report,

    "grade": grade_report,

    "breakdown": breakdown_report,

}