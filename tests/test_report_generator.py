from app.report.report_generator import ReportGenerator

generator = ReportGenerator()

report = generator.generate(

    "outputs/requirements.json",

    "outputs/validated_mapping.json",

    "outputs/validated_evaluation.json"

)

print(report["summary"])