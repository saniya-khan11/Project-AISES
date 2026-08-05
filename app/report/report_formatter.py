class ReportFormatter:
    """
    Formats the complete assessment report.

    Responsibilities
    ----------------
    - Build a structured report.
    - Organize report into sections.
    - Remain independent of output format.
    """

    # ==========================================================
    # Format Report
    # ==========================================================

    def format(
        self,
        report_context,
        executive_summary,
    ):
        """
        Formats the complete report.

        Parameters
        ----------
        report_context : dict
        executive_summary : dict

        Returns
        -------
        dict
        """

        metadata = report_context.get(
            "metadata",
            {},
        )

        # ======================================================
        # Report Sections
        # ======================================================

        sections = [

            {
                "id": 1,
                "title": "Executive Summary",
                "content": executive_summary,
            },

            {
                "id": 2,
                "title": "Requirement Assessment",
                "content": report_context.get(
                    "requirement",
                    {},
                ),
            },

            {
                "id": 3,
                "title": "Security Assessment",
                "content": report_context.get(
                    "security",
                    {},
                ),
            },

            {
                "id": 4,
                "title": "Performance Assessment",
                "content": report_context.get(
                    "performance",
                    {},
                ),
            },

            {
                "id": 5,
                "title": "Best Practice Assessment",
                "content": report_context.get(
                    "best_practice",
                    {},
                ),
            },

            {
                "id": 6,
                "title": "AI Evaluation",
                "content": report_context.get(
                    "ai_evaluation",
                    {},
                ),
            },

            {
                "id": 7,
                "title": "Overall Assessment",
                "content": report_context.get(
                    "overall_assessment",
                    {},
                ),
            },

            {
                "id": 8,
                "title": "Recommendations",
                "content": report_context.get(
                    "recommendations",
                    {},
                ),
            },

        ]

        # ======================================================
        # Build Report
        # ======================================================

        report = {

            # --------------------------------------------------
            # Metadata
            # --------------------------------------------------

            "title": metadata.get(
                "report_type",
                "Software Assessment Report",
            ),

            "generator": metadata.get(
                "generator",
                "AISES",
            ),

            "version": metadata.get(
                "version",
                "1.0",
            ),

            "generated_at": metadata.get(
                "generated_at",
                "",
            ),

            # --------------------------------------------------
            # Quick Summary
            # --------------------------------------------------

            "summary": {

                "project": executive_summary.get(
                    "project_name",
                ),

                "overall_score": executive_summary.get(
                    "overall_score",
                ),

                "grade": executive_summary.get(
                    "grade",
                ),

                "deployment_ready": executive_summary.get(
                    "status",
                    {},
                ).get(
                    "deployment_ready",
                ),

                "total_sections": len(sections),

            },

            # --------------------------------------------------
            # Table of Contents
            # --------------------------------------------------

            "table_of_contents": [

                {

                    "id": section["id"],

                    "title": section["title"],

                }

                for section in sections

            ],

            # --------------------------------------------------
            # Report Sections
            # --------------------------------------------------

            "sections": sections,

            # --------------------------------------------------
            # Report Statistics
            # --------------------------------------------------

            "section_count": len(sections),

        }

        return report