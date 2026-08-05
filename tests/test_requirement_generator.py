from app.requirement_generator.generator import RequirementGenerator

generator = RequirementGenerator()

requirements = generator.generate(
    "examples/sample_srs.txt"
)

print(requirements)