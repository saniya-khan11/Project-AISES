from app.mapper.requirement_mapper import RequirementMapper

mapper = RequirementMapper()

result = mapper.map(

    "outputs/requirements.json",

    "outputs/project_cst.json",

    "outputs/candidate_cst.json"

)

print(result)