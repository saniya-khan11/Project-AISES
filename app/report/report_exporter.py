import json


class ReportExporter:
    """
    Exports the formatted report into different formats.

    Supported Formats
    -----------------
    - text
    - markdown
    - json
    """

    SUPPORTED_FORMATS = (
        "text",
        "markdown",
        "json",
    )

    # ==========================================================
    # Export Report
    # ==========================================================

    def export(
        self,
        report,
        export_format="text",
    ):
        """
        Export report.

        Parameters
        ----------
        report : dict

        export_format : str

        Returns
        -------
        str
        """

        export_format = export_format.lower()

        if export_format not in self.SUPPORTED_FORMATS:

            raise ValueError(

                f"Unsupported export format: {export_format}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"

            )

        exporters = {

            "text": self._export_text,

            "markdown": self._export_markdown,

            "json": self._export_json,

        }

        return exporters[export_format](report)

    # ==========================================================
    # Text Export
    # ==========================================================

    def _export_text(
        self,
        report,
    ):

        lines = []

        lines.append(report["title"])

        lines.append("=" * len(report["title"]))

        lines.append("")

        summary = report["summary"]

        lines.append(
            f"Project : {summary['project']}"
        )

        lines.append(
            f"Overall Score : {summary['overall_score']}"
        )

        lines.append(
            f"Grade : {summary['grade']}"
        )

        lines.append(
            f"Deployment Ready : {summary['deployment_ready']}"
        )

        lines.append("")

        lines.append("TABLE OF CONTENTS")

        lines.append("-----------------")

        for item in report["table_of_contents"]:

            lines.append(
                f"{item['id']}. {item['title']}"
            )

        lines.append("")

        lines.append("REPORT SECTIONS")

        lines.append("-----------------")

        for section in report["sections"]:

            lines.append(
                f"[{section['id']}] {section['title']}"
            )

        return "\n".join(lines)

    # ==========================================================
    # Markdown Export
    # ==========================================================

    def _export_markdown(
        self,
        report,
    ):

        md = []

        md.append(f"# {report['title']}")

        md.append("")

        summary = report["summary"]

        md.append("## Executive Summary")

        md.append("")

        md.append(
            f"- **Project:** {summary['project']}"
        )

        md.append(
            f"- **Overall Score:** {summary['overall_score']}"
        )

        md.append(
            f"- **Grade:** {summary['grade']}"
        )

        md.append(
            f"- **Deployment Ready:** {summary['deployment_ready']}"
        )

        md.append("")

        md.append("## Table of Contents")

        md.append("")

        for item in report["table_of_contents"]:

            md.append(
                f"{item['id']}. {item['title']}"
            )

        md.append("")

        for section in report["sections"]:

            md.append(
                f"## {section['title']}"
            )

            md.append("")

            md.append("```json")

            md.append(

                json.dumps(

                    section["content"],

                    indent=4,

                )

            )

            md.append("```")

            md.append("")

        return "\n".join(md)

    # ==========================================================
    # JSON Export
    # ==========================================================

    def _export_json(
        self,
        report,
    ):

        return json.dumps(

            report,

            indent=4,

        )