from app.validator.evaluation_validator import EvaluationValidator

validator = EvaluationValidator()

validator.validate(

    "outputs/evaluation.json",

    "outputs/requirements.json"

)