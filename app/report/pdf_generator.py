import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


class PDFReportGenerator:
    """
    Generates a professional PDF report
    from AISES report.json
    """

    def generate(
        self,
        report_json="outputs/report.json",
        output_file="outputs/AISES_Report.pdf"
    ):

        with open(report_json, encoding="utf-8") as fp:
            report = json.load(fp)

        styles = getSampleStyleSheet()

        doc = SimpleDocTemplate(output_file)

        elements = []

        ############################################################

        elements.append(
            Paragraph(
                "<b><font size=22>AISES Software Evaluation Report</font></b>",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        ############################################################

        elements.append(
            Paragraph(
                "<b>Executive Summary</b>",
                styles["Heading1"]
            )
        )

        summary = report["summary"]

        summary_table = [

            ["Metric", "Value"],

            ["Total Requirements", summary["total_requirements"]],

            ["Implemented", summary["implemented"]],

            ["Partially Implemented", summary["partially_implemented"]],

            ["Not Implemented", summary["not_implemented"]],

            ["Overall Compliance", f"{summary['overall_compliance']} %"]

        ]

        table = Table(summary_table)

        table.setStyle(TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10)

        ]))

        elements.append(table)

        elements.append(Spacer(1, 25))

        ############################################################

        elements.append(

            Paragraph(

                "<b>Requirement Evaluation</b>",

                styles["Heading1"]

            )

        )

        ############################################################

        for req in report["requirements"]:

            elements.append(

                Paragraph(

                    f"<b>{req['ac_id']} : {req['requirement_title']}</b>",

                    styles["Heading2"]

                )

            )

            elements.append(

                Paragraph(

                    req["description"],

                    styles["BodyText"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Status :</b> {req['status']}",

                    styles["BodyText"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Coverage :</b> {req['coverage']} %",

                    styles["BodyText"]

                )

            )

            elements.append(

                Paragraph(

                    f"<b>Confidence :</b> {req['confidence']}",

                    styles["BodyText"]

                )

            )

            ########################################################

            elements.append(

                Paragraph(

                    "<b>Matched Files</b>",

                    styles["Heading3"]

                )

            )

            if req["matched_files"]:

                for file in req["matched_files"]:

                    elements.append(

                        Paragraph(

                            f"• {file}",

                            styles["BodyText"]

                        )

                    )

            else:

                elements.append(

                    Paragraph(

                        "None",

                        styles["BodyText"]

                    )

                )

            ########################################################

            elements.append(

                Paragraph(

                    "<b>Strengths</b>",

                    styles["Heading3"]

                )

            )

            if req["strengths"]:

                for item in req["strengths"]:

                    elements.append(

                        Paragraph(

                            f"• {item}",

                            styles["BodyText"]

                        )

                    )

            else:

                elements.append(

                    Paragraph(

                        "None",

                        styles["BodyText"]

                    )

                )

            ########################################################

            elements.append(

                Paragraph(

                    "<b>Issues</b>",

                    styles["Heading3"]

                )

            )

            if req["issues"]:

                for item in req["issues"]:

                    elements.append(

                        Paragraph(

                            f"• {item}",

                            styles["BodyText"]

                        )

                    )

            else:

                elements.append(

                    Paragraph(

                        "None",

                        styles["BodyText"]

                    )

                )

            ########################################################

            elements.append(

                Paragraph(

                    "<b>Recommendations</b>",

                    styles["Heading3"]

                )

            )

            if req["recommendations"]:

                for item in req["recommendations"]:

                    elements.append(

                        Paragraph(

                            f"• {item}",

                            styles["BodyText"]

                        )

                    )

            else:

                elements.append(

                    Paragraph(

                        "None",

                        styles["BodyText"]

                    )

                )

            elements.append(Spacer(1, 18))

        ############################################################

        doc.build(elements)

        print(f"Saved : {output_file}")

        return output_file