from pathlib import Path

from app.report.report_generator import ReportGenerator
from app.report.markdown_generator import MarkdownReportGenerator
from app.report.html_generator import HTMLReportGenerator
from app.report.pdf_generator import PDFReportGenerator


BASE_COMMIT = (
    "76dc6ae7cc1376ea67f8ad3f06125489e2e4888a"
)

TARGET_COMMIT = (
    "0a15a7fd7b030b9a06d511cd9d6add62259e8932"
)


def test_git_report_generator():

    base_dir = Path(
        "outputs"
    ) / "commits" / BASE_COMMIT

    target_dir = Path(
        "outputs"
    ) / "commits" / TARGET_COMMIT

    requirements_path = (
        base_dir / "requirements.json"
    )

    mapping_path = (
        target_dir / "validated_mapping.json"
    )

    evaluation_path = (
        target_dir / "validated_evaluation.json"
    )

    report_path = (
        target_dir / "report.json"
    )

    markdown_path = (
        target_dir / "report.md"
    )

    html_path = (
        target_dir / "report.html"
    )

    pdf_path = (
        target_dir / "AISES_Report.pdf"
    )

    print()
    print("=" * 80)
    print("GIT TARGET COMMIT REPORT GENERATION")
    print("=" * 80)

    print()
    print("Base Commit:")
    print(BASE_COMMIT)

    print()
    print("Target Commit:")
    print(TARGET_COMMIT)

    print()
    print("Requirements:")
    print(requirements_path)

    print()
    print("Merged Mapping:")
    print(mapping_path)

    print()
    print("Merged Evaluation:")
    print(evaluation_path)

    ############################################################
    # 1. JSON Report
    ############################################################

    print()
    print("[1/4] Report Generator")

    ReportGenerator().generate(
        str(requirements_path),
        str(mapping_path),
        str(evaluation_path),
        str(report_path),
    )

    ############################################################
    # 2. Markdown Report
    ############################################################

    print()
    print("[2/4] Markdown Report Generator")

    MarkdownReportGenerator().generate(
        str(report_path),
        str(markdown_path),
    )

    ############################################################
    # 3. HTML Report
    ############################################################

    print()
    print("[3/4] HTML Report Generator")

    HTMLReportGenerator().generate(
        str(report_path),
        str(html_path),
    )

    ############################################################
    # 4. PDF Report
    ############################################################

    print()
    print("[4/4] PDF Report Generator")

    PDFReportGenerator().generate(
        str(report_path),
        str(pdf_path),
    )

    print()
    print("=" * 80)
    print("TARGET COMMIT REPORT GENERATED")
    print("=" * 80)

    print()
    print("Generated Files")
    print("-" * 80)

    print(report_path)
    print(markdown_path)
    print(html_path)
    print(pdf_path)


if __name__ == "__main__":
    test_git_report_generator()