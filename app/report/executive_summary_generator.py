class ExecutiveSummaryGenerator:
    """
    Generates the executive summary for the assessment report.

    Responsibilities
    ----------------
    - Produce a concise management-level summary.
    - Extract key information from the report context.
    - Generate dashboard highlights.
    - Generate project status indicators.
    """

    # ==========================================================
    # Generate Executive Summary
    # ==========================================================

    def generate(self, report_context):
        """
        Generates the executive summary.

        Parameters
        ----------
        report_context : dict

        Returns
        -------
        dict
        """

        project = report_context.get("project", {})

        requirement = report_context.get(
            "requirement", {}
        ).get(
            "summary", {}
        )

        security = report_context.get(
            "security", {}
        ).get(
            "summary", {}
        )

        performance = report_context.get(
            "performance", {}
        ).get(
            "summary", {}
        )

        best_practice = report_context.get(
            "best_practice", {}
        ).get(
            "summary", {}
        )

        overall = report_context.get(
            "overall_assessment", {}
        )

        recommendations = report_context.get(
            "recommendations", {}
        ).get(
            "summary", {}
        )

        metadata = report_context.get(
            "metadata", {}
        )

        overall_score = overall.get(
            "overall_score",
            0,
        )

        grade = overall.get(
            "grade",
            "UNKNOWN",
        )

        deployment = overall.get(
            "deployment_recommendation",
            "Not Available",
        ).rstrip(".")

        summary = {

            # --------------------------------------------------
            # Project Information
            # --------------------------------------------------

            "project_name": project.get(
                "name",
                "Unknown",
            ),

            "programming_language": project.get(
                "language",
                "Unknown",
            ),

            # --------------------------------------------------
            # Overall Assessment
            # --------------------------------------------------

            "overall_score": overall_score,

            "grade": grade,

            "deployment_recommendation": deployment,

            # --------------------------------------------------
            # Requirement Assessment
            # --------------------------------------------------

            "requirement_status": requirement.get(
                "status",
                "Unknown",
            ),

            "requirement_confidence": requirement.get(
                "confidence",
                0,
            ),

            # --------------------------------------------------
            # Security Assessment
            # --------------------------------------------------

            "security_risk": security.get(
                "risk",
                "Unknown",
            ),

            "security_score": security.get(
                "security_score",
                0,
            ),

            # --------------------------------------------------
            # Performance Assessment
            # --------------------------------------------------

            "performance_rating": performance.get(
                "risk",
                "Unknown",
            ),

            "performance_score": performance.get(
                "performance_score",
                0,
            ),

            # --------------------------------------------------
            # Best Practice Assessment
            # --------------------------------------------------

            "best_practice_quality": best_practice.get(
                "quality",
                "Unknown",
            ),

            "best_practice_score": best_practice.get(
                "best_practice_score",
                0,
            ),

            # --------------------------------------------------
            # Recommendations
            # --------------------------------------------------

            "total_recommendations": recommendations.get(
                "total_recommendations",
                0,
            ),

            # --------------------------------------------------
            # Metadata
            # --------------------------------------------------

            "generated_at": metadata.get(
                "generated_at",
                "",
            ),

            "report_type": metadata.get(
                "report_type",
                "",
            ),

            "generator": metadata.get(
                "generator",
                "",
            ),

            # --------------------------------------------------
            # Dashboard Highlights
            # --------------------------------------------------

            "highlights": {

                "overall_score": overall_score,

                "grade": grade,

                "security": security.get(
                    "risk",
                    "Unknown",
                ),

                "performance": performance.get(
                    "risk",
                    "Unknown",
                ),

                "requirements": requirement.get(
                    "status",
                    "Unknown",
                ),

                "recommendations": recommendations.get(
                    "total_recommendations",
                    0,
                ),

            },

            # --------------------------------------------------
            # Project Status
            # --------------------------------------------------

            "status": {

                "overall": (
                    "PASS"
                    if overall_score >= 70
                    else "REVIEW"
                ),

                "grade": grade,

                "overall_score": overall_score,

                "deployment_ready": (
                    "not recommended"
                    not in deployment.lower()
                ),

                "requirement_status": requirement.get(
                    "status",
                    "Unknown",
                ),

                "security_risk": security.get(
                    "risk",
                    "Unknown",
                ),

                "performance_rating": performance.get(
                    "risk",
                    "Unknown",
                ),

                "best_practice_quality": best_practice.get(
                    "quality",
                    "Unknown",
                ),

            },

            # --------------------------------------------------
            # Human Readable Executive Summary
            # --------------------------------------------------

            "executive_summary": self._build_summary(

                project_name=project.get(
                    "name",
                    "Unknown",
                ),

                overall_score=overall_score,

                grade=grade,

                deployment=deployment,

                security=security.get(
                    "risk",
                    "Unknown",
                ),

                performance=performance.get(
                    "risk",
                    "Unknown",
                ),

                requirement=requirement.get(
                    "status",
                    "Unknown",
                ),

                recommendations=recommendations.get(
                    "total_recommendations",
                    0,
                ),

            ),

        }

        return summary

    # ==========================================================
    # Build Human Readable Summary
    # ==========================================================

    def _build_summary(
        self,
        project_name,
        overall_score,
        grade,
        deployment,
        security,
        performance,
        requirement,
        recommendations,
    ):
        """
        Creates a human-readable executive summary.
        """

        return (

            f"Project '{project_name}' achieved an overall score of "

            f"{overall_score}/100 with a grade of {grade}. "

            f"Requirement implementation status is "

            f"'{requirement}'. "

            f"Security risk is '{security}' and "

            f"performance is rated '{performance}'. "

            f"{recommendations} recommendation(s) "

            f"were generated. "

            f"Deployment recommendation: "

            f"{deployment}."

        )