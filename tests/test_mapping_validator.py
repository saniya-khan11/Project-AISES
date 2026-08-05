from app.validator.mapping_validator import MappingValidator

validator = MappingValidator()

validator.validate(

    "outputs/mapping.json",

    "outputs/project_cst.json"

)