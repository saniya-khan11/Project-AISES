from app.agents.ollama_client import OllamaClient
from app.extra_features.extra_feature_prompt import ExtraFeaturePrompt
from app.extra_features.extra_feature_parser import ExtraFeatureParser


class LLMExtraFeatureDetector:

    def __init__(self):
        print("1. Constructor")

        self.llm = OllamaClient()

        self.prompt_builder = ExtraFeaturePrompt()

        self.parser = ExtraFeatureParser()

        print("2. Constructor finished")

    def detect(self, requirement, capability):

        print("3. Inside detect()")

        prompt = self.prompt_builder.build(
            requirement,
            capability
        )

        print("4. Prompt created")
        print(prompt)

        response = self.llm.ask(prompt)

        print("5. Response received")
        print(response)

        result = self.parser.parse(response)

        print("6. Parsed")

        return result