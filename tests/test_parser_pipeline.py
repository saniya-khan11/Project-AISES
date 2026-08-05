from app.parser.parser_pipeline import ParserPipeline

pipeline = ParserPipeline()

project = pipeline.process(
    "examples/sample_project"
)

print(project["project"])