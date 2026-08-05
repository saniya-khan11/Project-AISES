import json
from pathlib import Path


class ConfigLoader:

    def __init__(self):

        config_path = Path(__file__).parent / "config.json"

        with open(config_path, "r", encoding="utf-8") as fp:
            self.config = json.load(fp)

    def get(self, key, default=None):

        return self.config.get(key, default)

    def all(self):

        return self.config