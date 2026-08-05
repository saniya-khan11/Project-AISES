from app.config.config_loader import ConfigLoader

from app.mapper.requirement_mapper import RequirementMapper
from app.validator.mapping_validator import MappingValidator
from app.evaluator.requirement_evaluator import RequirementEvaluator
from app.validator.evaluation_validator import EvaluationValidator
from app.report.report_generator import ReportGenerator


def main():

    print("=" * 80)
    print("AISES - MAPPER / EVALUATOR TEST")
    print("=" * 80)

    config = ConfigLoader()

    output_dir = config.get("output_directory")

    ############################################################
    # Requirement Mapper
    ############################################################

    print("\n[1/5] Requirement Mapper")

    RequirementMapper().map(
        f"{output_dir}/requirements.json",
        f"{output_dir}/project_cst.json",
        f"{output_dir}/candidate_cst.json",
        f"{output_dir}/mapping.json"
    )

    ############################################################
    # Mapping Validator
    ############################################################

    print("\n[2/5] Mapping Validator")

    MappingValidator().validate(
        f"{output_dir}/mapping.json",
        f"{output_dir}/project_cst.json",
        f"{output_dir}/validated_mapping.json"
    )

    ############################################################
    # Requirement Evaluator
    ############################################################

    print("\n[3/5] Requirement Evaluator")

    RequirementEvaluator().evaluate(
        f"{output_dir}/requirements.json",
        f"{output_dir}/validated_mapping.json",
        f"{output_dir}/project_cst.json",
        f"{output_dir}/evaluation.json"
    )

    ############################################################
    # Evaluation Validator
    ############################################################

    print("\n[4/5] Evaluation Validator")

    EvaluationValidator().validate(
        f"{output_dir}/evaluation.json",
        f"{output_dir}/requirements.json",
        f"{output_dir}/validated_evaluation.json"
    )

    ############################################################
    # Report Generator
    ############################################################

    print("\n[5/5] Report Generator")

    ReportGenerator().generate(
        f"{output_dir}/requirements.json",
        f"{output_dir}/validated_mapping.json",
        f"{output_dir}/validated_evaluation.json",
        f"{output_dir}/report.json"
    )

    print("\n" + "=" * 80)
    print("MAPPER / EVALUATOR TEST COMPLETED")
    print("=" * 80)

    print("\nGenerated Files")
    print("-" * 80)

    files = [
        "mapping.json",
        "validated_mapping.json",
        "evaluation.json",
        "validated_evaluation.json",
        "report.json"
    ]

    for file in files:
        print(f"✓ {output_dir}/{file}")


if __name__ == "__main__":
    main()