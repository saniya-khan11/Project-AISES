from app.config.config_loader import ConfigLoader

from app.logger.logger import AISESLogger

from app.requirement_generator.generator import RequirementGenerator
from app.parser.parser_pipeline import ParserPipeline
from app.retriever.candidate_retriever import CandidateRetriever
from app.mapper.requirement_mapper import RequirementMapper
from app.validator.mapping_validator import MappingValidator
from app.evaluator.requirement_evaluator import RequirementEvaluator
from app.validator.evaluation_validator import EvaluationValidator

from app.report.report_generator import ReportGenerator
from app.report.markdown_generator import MarkdownReportGenerator
from app.report.html_generator import HTMLReportGenerator
from app.report.pdf_generator import PDFReportGenerator


def main():

    print("=" * 80)
    print("AISES - AI SOFTWARE EVALUATION SYSTEM")
    print("=" * 80)

    logger = AISESLogger.get_logger()

    logger.info("=" * 80)
    logger.info("AISES EXECUTION STARTED")

    ############################################################
    # Load Configuration
    ############################################################

    config = ConfigLoader()

    srs_file = config.get("srs_file")
    source_code_folder = config.get("source_code_folder")
    output_dir = config.get("output_directory")

    print("\nProject Configuration")
    print("-" * 80)
    print(f"SRS File          : {srs_file}")
    print(f"Source Code Folder: {source_code_folder}")
    print(f"Output Directory  : {output_dir}")

    logger.info("Configuration Loaded")

    ############################################################
    # Module 1
    ############################################################

    print("\n[1/12] Requirement Generator")

    RequirementGenerator().generate(
        srs_file,
        f"{output_dir}/requirements.json"
    )

    logger.info("Requirement Generator completed.")

    ############################################################
    # Module 2
    ############################################################

    print("\n[2/12] Tree-sitter Parser")

    ParserPipeline().process(
        source_code_folder,
        f"{output_dir}/project_cst.json"
    )

    logger.info("Tree-sitter Parser completed.")

    ############################################################
    # Module 3
    ############################################################

    print("\n[3/12] Candidate Retriever")

    CandidateRetriever().retrieve(
        f"{output_dir}/requirements.json",
        f"{output_dir}/project_cst.json",
        f"{output_dir}/candidate_cst.json"
    )

    logger.info("Candidate Retriever completed.")

    ############################################################
    # Module 4
    ############################################################

    print("\n[4/12] Requirement Mapper")

    RequirementMapper().map(
        f"{output_dir}/requirements.json",
        f"{output_dir}/project_cst.json",
        f"{output_dir}/candidate_cst.json",
        f"{output_dir}/mapping.json"
    )

    logger.info("Requirement Mapper completed.")

    ############################################################
    # Module 5
    ############################################################

    print("\n[5/12] Mapping Validator")

    MappingValidator().validate(
        f"{output_dir}/mapping.json",
        f"{output_dir}/project_cst.json",
        f"{output_dir}/validated_mapping.json"
    )

    logger.info("Mapping Validator completed.")

    ############################################################
    # Module 6
    ############################################################

    print("\n[6/12] Requirement Evaluator")

    RequirementEvaluator().evaluate(
        f"{output_dir}/requirements.json",
        f"{output_dir}/validated_mapping.json",
        f"{output_dir}/project_cst.json",
        f"{output_dir}/evaluation.json"
    )

    logger.info("Requirement Evaluator completed.")

    ############################################################
    # Module 7
    ############################################################

    print("\n[7/12] Evaluation Validator")

    EvaluationValidator().validate(
        f"{output_dir}/evaluation.json",
        f"{output_dir}/requirements.json",
        f"{output_dir}/validated_evaluation.json"
    )

    logger.info("Evaluation Validator completed.")

    ############################################################
    # Module 8
    ############################################################

    print("\n[8/12] Report Generator")

    ReportGenerator().generate(
        f"{output_dir}/requirements.json",
        f"{output_dir}/validated_mapping.json",
        f"{output_dir}/validated_evaluation.json",
        f"{output_dir}/report.json"
    )

    logger.info("Report Generator completed.")

    ############################################################
    # Module 9
    ############################################################

    print("\n[9/12] Markdown Report Generator")

    MarkdownReportGenerator().generate(
        f"{output_dir}/report.json",
        f"{output_dir}/report.md"
    )

    logger.info("Markdown Report generated.")

    ############################################################
    # Module 10
    ############################################################

    print("\n[10/12] HTML Report Generator")

    HTMLReportGenerator().generate(
        f"{output_dir}/report.json",
        f"{output_dir}/report.html"
    )

    logger.info("HTML Report generated.")

    ############################################################
    # Module 11
    ############################################################

    print("\n[11/12] PDF Report Generator")

    PDFReportGenerator().generate(
        f"{output_dir}/report.json",
        f"{output_dir}/AISES_Report.pdf"
    )

    logger.info("PDF Report generated.")

    ############################################################
    # Module 12
    ############################################################

    print("\n[12/12] Finalizing")

    logger.info("AISES EXECUTION COMPLETED SUCCESSFULLY")
    logger.info("=" * 80)

    print("\n" + "=" * 80)
    print("AISES EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 80)

    print("\nGenerated Files")
    print("-" * 80)

    generated_files = [
        "requirements.json",
        "project_cst.json",
        "candidate_cst.json",
        "mapping.json",
        "validated_mapping.json",
        "evaluation.json",
        "validated_evaluation.json",
        "report.json",
        "report.md",
        "report.html",
        "AISES_Report.pdf"
    ]

    for file in generated_files:
        print(f"✓ {output_dir}/{file}")

    print("\nLogs")
    print("-" * 80)
    print("✓ outputs/logs/aises.log")

    print("\nThank you for using AISES.")


if __name__ == "__main__":
    main()