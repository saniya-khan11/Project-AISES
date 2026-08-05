from datetime import datetime, timezone


class ReportContextBuilder:
    """
    Builds the complete report context.

    Responsibilities
    ----------------
    - Collect outputs from all assessment modules.
    - Produce a standardized report context.
    - Add report metadata.
    """

    REPORT_TYPE = "Software Implementation Assessment Report"

    GENERATOR = "AISES"

    VERSION = "1.0"

    MODULES = [

        "Requirement Assessment",

        "Security Assessment",

        "Performance Assessment",

        "Best Practice Assessment",

        "AI Evaluation",

        "Overall Assessment",

        "Recommendation Engine",

    ]

    # ==========================================================
    # Build Report Context
    # ==========================================================

    def build(
        self,
        project,
        requirement_assessment,
        security_assessment,
        performance_assessment,
        best_practice_assessment,
        ai_evaluation,
        overall_assessment,
        recommendation_report,
    ):
        """
        Builds the complete report context.

        Parameters
        ----------
        project : dict
        requirement_assessment : dict
        security_assessment : dict
        performance_assessment : dict
        best_practice_assessment : dict
        ai_evaluation : dict
        overall_assessment : dict
        recommendation_report : dict

        Returns
        -------
        dict
        """

        generated_at = (

            datetime.now(timezone.utc)

            .replace(microsecond=0)

            .isoformat()

        )

        return {

            # ==================================================
            # Project Information
            # ==================================================

            "project": project,

            # ==================================================
            # Assessment Modules
            # ==================================================

            "requirement": requirement_assessment,

            "security": security_assessment,

            "performance": performance_assessment,

            "best_practice": best_practice_assessment,

            "ai_evaluation": ai_evaluation,

            "overall_assessment": overall_assessment,

            "recommendations": recommendation_report,

            # ==================================================
            # Metadata
            # ==================================================

            "metadata": {

                "generator": self.GENERATOR,

                "report_type": self.REPORT_TYPE,

                "version": self.VERSION,

                "generated_at": generated_at,

                "modules": self.MODULES,

            },

        }