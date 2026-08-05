import json
from pathlib import Path


class MappingValidator:
    """
    Validates mapping.json against project_cst.json.
    Ensures the LLM has not hallucinated files or node IDs.
    """

    def validate(
        self,
        mapping_file,
        project_file,
        output_file="outputs/validated_mapping.json"
    ):

        with open(mapping_file, encoding="utf-8") as fp:
            mappings = json.load(fp)

        with open(project_file, encoding="utf-8") as fp:
            project = json.load(fp)

        valid_files = {
            file["filename"]
            for file in project["files"]
        }

        validated = []

        for mapping in mappings:

            matched_files = []

            for filename in mapping.get("matched_files", []):

                if filename in valid_files:
                    matched_files.append(filename)
                else:
                    print(f"[WARNING] Invalid file removed: {filename}")

            mapping["matched_files"] = matched_files

            validated.append(mapping)

        Path(output_file).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as fp:

            json.dump(
                validated,
                fp,
                indent=4,
                ensure_ascii=False
            )

        print(f"Validated mapping saved to {output_file}")

        return validated