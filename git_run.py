import sys
from pathlib import Path

from app.git.diff_analyzer import DiffAnalyzer
from app.git.changed_node_analyzer import ChangedNodeAnalyzer
from app.git.impact_analyzer import ImpactAnalyzer
from app.git.evaluation_selector import EvaluationSelector
from app.git.requirement_filter import RequirementFilter
from app.git.mapping_merger import MappingMerger
from app.git.evaluation_merger import EvaluationMerger

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


# ============================================================
# Repository Configuration
# ============================================================

REPOSITORY_PATH = Path(
    r"C:\Users\lenovo\Desktop\test-git-repos\calculator"
)

OUTPUT_ROOT = Path("outputs")

COMMIT_OUTPUT_ROOT = OUTPUT_ROOT / "commits"


# ============================================================
# Selective Target Evaluation
# ============================================================

def run_selective_evaluation(
    requirements_path,
    source_code_folder,
    output_dir,
):
    """
    Runs the normal mapping/evaluation pipeline only for
    requirements selected for re-evaluation.
    """

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    project_cst_path = (
        output_dir / "project_cst.json"
    )

    candidate_cst_path = (
        output_dir / "candidate_cst.json"
    )

    mapping_path = (
        output_dir / "mapping.json"
    )

    validated_mapping_path = (
        output_dir / "validated_mapping.json"
    )

    evaluation_path = (
        output_dir / "evaluation.json"
    )

    validated_evaluation_path = (
        output_dir / "validated_evaluation.json"
    )

    # --------------------------------------------------------
    # Parser
    # --------------------------------------------------------

    print("\n[6/11] Tree-sitter Parser")

    ParserPipeline().process(
        str(source_code_folder),
        str(project_cst_path),
    )

    # --------------------------------------------------------
    # Candidate Retriever
    # --------------------------------------------------------

    print("\n[7/11] Candidate Retriever")

    CandidateRetriever().retrieve(
        str(requirements_path),
        str(project_cst_path),
        str(candidate_cst_path),
    )

    # --------------------------------------------------------
    # Requirement Mapper
    # --------------------------------------------------------

    print("\n[8/11] Requirement Mapper")

    RequirementMapper().map(
        str(requirements_path),
        str(project_cst_path),
        str(candidate_cst_path),
        str(mapping_path),
    )

    # --------------------------------------------------------
    # Mapping Validator
    # --------------------------------------------------------

    print("\n[9/11] Mapping Validator")

    MappingValidator().validate(
        str(mapping_path),
        str(project_cst_path),
        str(validated_mapping_path),
    )

    # --------------------------------------------------------
    # Requirement Evaluator
    # --------------------------------------------------------

    print("\n[10/11] Requirement Evaluator")

    RequirementEvaluator().evaluate(
        str(requirements_path),
        str(validated_mapping_path),
        str(project_cst_path),
        str(evaluation_path),
    )

    # --------------------------------------------------------
    # Evaluation Validator
    # --------------------------------------------------------

    print("\n[11/11] Evaluation Validator")

    EvaluationValidator().validate(
        str(evaluation_path),
        str(requirements_path),
        str(validated_evaluation_path),
    )

    return {
        "project_cst": project_cst_path,
        "candidate_cst": candidate_cst_path,
        "mapping": mapping_path,
        "validated_mapping": validated_mapping_path,
        "evaluation": evaluation_path,
        "validated_evaluation": validated_evaluation_path,
    }


# ============================================================
# Final Report Generation
# ============================================================

def generate_final_report(
    requirements_path,
    mapping_path,
    evaluation_path,
    target_dir,
):
    """
    Generates the complete report for the target commit
    after reused and re-evaluated results have been merged.
    """

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
    print("FINAL TARGET REPORT GENERATION")
    print("=" * 80)

    print("\n[1/4] Report Generator")

    ReportGenerator().generate(
        str(requirements_path),
        str(mapping_path),
        str(evaluation_path),
        str(report_path),
    )

    print("\n[2/4] Markdown Report")

    MarkdownReportGenerator().generate(
        str(report_path),
        str(markdown_path),
    )

    print("\n[3/4] HTML Report")

    HTMLReportGenerator().generate(
        str(report_path),
        str(html_path),
    )

    print("\n[4/4] PDF Report")

    PDFReportGenerator().generate(
        str(report_path),
        str(pdf_path),
    )

    return {
        "report": report_path,
        "markdown": markdown_path,
        "html": html_path,
        "pdf": pdf_path,
    }


# ============================================================
# Main Git Evaluation Pipeline
# ============================================================

def run_git_evaluation(
    base_commit,
    target_commit,
):

    print()
    print("=" * 80)
    print("DEVGROW AI EVALUATOR V2")
    print("GIT INCREMENTAL EVALUATION")
    print("=" * 80)

    print()
    print("Repository")
    print("-" * 80)
    print(REPOSITORY_PATH)

    print()
    print("Base Commit")
    print("-" * 80)
    print(base_commit)

    print()
    print("Target Commit")
    print("-" * 80)
    print(target_commit)

    # ========================================================
    # Paths
    # ========================================================

    base_dir = (
        COMMIT_OUTPUT_ROOT / base_commit
    )

    target_dir = (
        COMMIT_OUTPUT_ROOT / target_commit
    )

    reevaluation_dir = (
        target_dir / "reevaluation"
    )

    target_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Base snapshot files

    base_requirements_path = (
        base_dir / "requirements.json"
    )

    base_mapping_path = (
        base_dir / "validated_mapping.json"
    )

    base_evaluation_path = (
        base_dir / "validated_evaluation.json"
    )

    # Temporary Git analysis outputs

    git_diff_path = (
        OUTPUT_ROOT / "git_diff.json"
    )

    changed_nodes_path = (
        OUTPUT_ROOT / "changed_nodes.json"
    )

    impact_analysis_path = (
        OUTPUT_ROOT / "impact_analysis.json"
    )

    evaluation_selection_path = (
        OUTPUT_ROOT / "evaluation_selection.json"
    )

    target_requirements_path = (
        OUTPUT_ROOT / "target_requirements.json"
    )

    # Final target artifacts

    merged_mapping_path = (
        target_dir / "validated_mapping.json"
    )

    merged_evaluation_path = (
        target_dir / "validated_evaluation.json"
    )

    # ========================================================
    # Validate Base Snapshot
    # ========================================================

    required_base_files = [
        base_requirements_path,
        base_mapping_path,
        base_evaluation_path,
    ]

    for path in required_base_files:

        if not path.exists():

            raise FileNotFoundError(
                "\nBase commit evaluation artifact missing:\n"
                f"{path}\n\n"
                "Run a full evaluation for the base commit "
                "and save its outputs first."
            )

    # ========================================================
    # STEP 1 — Git Diff
    # ========================================================

    print()
    print("=" * 80)
    print("[1/11] Git Diff Analysis")
    print("=" * 80)

    diff_analyzer = DiffAnalyzer(
        REPOSITORY_PATH
    )

    git_diff = diff_analyzer.analyze(
        base_commit,
        target_commit,
    )

    diff_analyzer.save_result(
        git_diff,
        git_diff_path,
    )

    print(
        f"Changed files: "
        f"{len(git_diff.get('changes', []))}"
    )

    # ========================================================
    # STEP 2 — Changed Node Analysis
    # ========================================================

    print()
    print("=" * 80)
    print("[2/11] Changed Node Analysis")
    print("=" * 80)

    changed_node_analyzer = (
        ChangedNodeAnalyzer()
    )

    changed_nodes = (
        changed_node_analyzer.analyze(
            git_diff_path=str(
                git_diff_path
            ),
            repository_path=str(
                REPOSITORY_PATH
            ),
        )
    )

    changed_node_analyzer.save_result(
        changed_nodes,
        changed_nodes_path,
    )

    # ========================================================
    # STEP 3 — Requirement Impact Analysis
    # ========================================================

    print()
    print("=" * 80)
    print("[3/11] Requirement Impact Analysis")
    print("=" * 80)

    impact_analyzer = ImpactAnalyzer()

    impact_result = impact_analyzer.analyze(
        git_diff_path=str(
            git_diff_path
        ),
        mapping_path=str(
            base_mapping_path
        ),
        changed_nodes_path=str(
            changed_nodes_path
        ),
    )

    impact_analyzer.save_result(
        impact_result,
        impact_analysis_path,
    )

    for requirement in impact_result.get(
        "requirements",
        [],
    ):
        print(
            f"{requirement.get('ac_id')}: "
            f"{requirement.get('status')}"
        )

    # ========================================================
    # STEP 4 — Evaluation Selection
    # ========================================================

    print()
    print("=" * 80)
    print("[4/11] Evaluation Selection")
    print("=" * 80)

    selector = EvaluationSelector()

    selection = selector.select(
        str(impact_analysis_path)
    )

    selector.save_result(
        selection,
        evaluation_selection_path,
    )

    reevaluate_ac_ids = (
        selection.get(
            "reevaluate_ac_ids",
            [],
        )
    )

    reuse_ac_ids = (
        selection.get(
            "reuse_ac_ids",
            [],
        )
    )

    print()
    print(
        "Requirements to re-evaluate:",
        len(reevaluate_ac_ids),
    )

    for ac_id in reevaluate_ac_ids:
        print(f"  {ac_id}")

    print()
    print(
        "Requirements safe to reuse:",
        len(reuse_ac_ids),
    )

    for ac_id in reuse_ac_ids:
        print(f"  {ac_id}")

    # ========================================================
    # STEP 5 — Requirement Filtering
    # ========================================================

    print()
    print("=" * 80)
    print("[5/11] Requirement Filtering")
    print("=" * 80)

    requirement_filter = (
        RequirementFilter()
    )

    filtered_requirements = (
        requirement_filter.filter(
            requirements_path=str(
                base_requirements_path
            ),
            selection_path=str(
                evaluation_selection_path
            ),
        )
    )

    requirement_filter.save_result(
        filtered_requirements,
        target_requirements_path,
    )

    selected_count = len(
        filtered_requirements.get(
            "acceptance_criteria",
            [],
        )
    )

    print(
        "Selected requirements:",
        selected_count,
    )

    # ========================================================
    # STEP 6–11 — Selective Target Evaluation
    # ========================================================

    selective_outputs = (
        run_selective_evaluation(
            requirements_path=(
                target_requirements_path
            ),
            source_code_folder=(
                REPOSITORY_PATH
            ),
            output_dir=(
                reevaluation_dir
            ),
        )
    )

    # ========================================================
    # Merge Mapping
    # ========================================================

    print()
    print("=" * 80)
    print("MERGING TARGET MAPPINGS")
    print("=" * 80)

    mapping_merger = (
        MappingMerger()
    )

    merged_mapping = (
        mapping_merger.merge(
            base_mapping_path=str(
                base_mapping_path
            ),
            target_mapping_path=str(
                selective_outputs[
                    "validated_mapping"
                ]
            ),
            selection_path=str(
                evaluation_selection_path
            ),
        )
    )

    mapping_merger.save_result(
        merged_mapping,
        merged_mapping_path,
    )

    print(
        "Merged mappings:",
        len(merged_mapping),
    )

    # ========================================================
    # Merge Evaluation
    # ========================================================

    print()
    print("=" * 80)
    print("MERGING TARGET EVALUATIONS")
    print("=" * 80)

    evaluation_merger = (
        EvaluationMerger()
    )

    merged_evaluation = (
        evaluation_merger.merge(
            base_evaluation_path=str(
                base_evaluation_path
            ),
            target_evaluation_path=str(
                selective_outputs[
                    "validated_evaluation"
                ]
            ),
            selection_path=str(
                evaluation_selection_path
            ),
        )
    )

    evaluation_merger.save_result(
        merged_evaluation,
        merged_evaluation_path,
    )

    print(
        "Merged evaluations:",
        len(merged_evaluation),
    )

    # ========================================================
    # Final Report
    # ========================================================

    report_files = generate_final_report(
        requirements_path=(
            base_requirements_path
        ),
        mapping_path=(
            merged_mapping_path
        ),
        evaluation_path=(
            merged_evaluation_path
        ),
        target_dir=(
            target_dir
        ),
    )

    # ========================================================
    # Completion
    # ========================================================

    print()
    print("=" * 80)
    print(
        "GIT INCREMENTAL EVALUATION COMPLETED"
    )
    print("=" * 80)

    print()
    print("Summary")
    print("-" * 80)

    print(
        f"Base Commit       : {base_commit}"
    )

    print(
        f"Target Commit     : {target_commit}"
    )

    print(
        f"Total Requirements: "
        f"{len(merged_evaluation)}"
    )

    print(
        f"Re-evaluated      : "
        f"{len(reevaluate_ac_ids)}"
    )

    print(
        f"Reused            : "
        f"{len(reuse_ac_ids)}"
    )

    print()
    print("Final Target Artifacts")
    print("-" * 80)

    print(
        f"Mapping    : "
        f"{merged_mapping_path}"
    )

    print(
        f"Evaluation : "
        f"{merged_evaluation_path}"
    )

    print(
        f"Report     : "
        f"{report_files['report']}"
    )

    print(
        f"Markdown   : "
        f"{report_files['markdown']}"
    )

    print(
        f"HTML       : "
        f"{report_files['html']}"
    )

    print(
        f"PDF        : "
        f"{report_files['pdf']}"
    )

    print()
    print("=" * 80)


# ============================================================
# CLI
# ============================================================

def main():

    if len(sys.argv) != 3:

        print()
        print(
            "Usage:"
        )

        print(
            "python git_run.py "
            "<base_commit> "
            "<target_commit>"
        )

        print()

        sys.exit(1)

    base_commit = sys.argv[1]

    target_commit = sys.argv[2]

    run_git_evaluation(
        base_commit,
        target_commit,
    )


if __name__ == "__main__":
    main()