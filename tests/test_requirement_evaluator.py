from app.evaluator.requirement_evaluator import RequirementEvaluator

evaluator = RequirementEvaluator()

result = evaluator.evaluate(

    "outputs/requirements.json",

    "outputs/mapping.json",

    "outputs/project_cst.json"

)

print(result)