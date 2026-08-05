import inspect
import json
from pathlib import Path
from typing import Any, Dict

from app.parser.project_loader import ProjectLoader
from app.parser.tree_sitter_parser import TreeSitterParser
from app.parser.cst_serializer import CSTSerializer


class ParserPipeline:
    """
    Loads project source files, parses them with Tree-sitter,
    and stores source code plus serialized CST data.

    The pipeline supports both parser styles:

    1. parse(file)
    2. parse(source_code, language)
    """

    def __init__(self) -> None:
        self.loader = ProjectLoader()
        self.parser = TreeSitterParser()
        self.serializer = CSTSerializer()

    def process(
        self,
        project_path: str,
        output_file: str = "outputs/project_cst.json",
    ) -> Dict[str, Any]:
        print("=" * 80)
        print("TREE-SITTER PARSER")
        print("=" * 80)

        files = self.loader.load(project_path)

        result: Dict[str, Any] = {
            "project": {
                "project_name": Path(project_path).name,
                "total_files": len(files),
                "languages": sorted(
                    {
                        file_data["language"]
                        for file_data in files
                    }
                ),
            },
            "files": [],
        }

        for file_data in files:
            print(f"Parsing : {file_data['path']}")

            try:
                parsed_result = self._parse_file(file_data)
                serialized_cst = self._serialize_result(
                    parsed_result
                )

                result["files"].append(
                    {
                        "file_id": file_data["file_id"],
                        "filename": file_data["filename"],
                        "path": file_data["path"],
                        "extension": file_data["extension"],
                        "language": file_data["language"],
                        "size": file_data["size"],
                        "parse_status": "SUCCESS",

                        # These two keys are essential for the
                        # retriever, mapper and evaluator.
                        "source_code": file_data["source_code"],
                        "cst": serialized_cst,
                    }
                )

                print(
                    f"Success : {file_data['filename']}"
                )

            except Exception as error:
                print(
                    f"Failed  : {file_data['path']} | {error}"
                )

                result["files"].append(
                    {
                        "file_id": file_data["file_id"],
                        "filename": file_data["filename"],
                        "path": file_data["path"],
                        "extension": file_data["extension"],
                        "language": file_data["language"],
                        "size": file_data["size"],
                        "parse_status": "FAILED",

                        # Preserve the source even when CST parsing
                        # fails, so later stages can still inspect it.
                        "source_code": file_data.get(
                            "source_code",
                            "",
                        ),
                        "cst": None,
                        "error": str(error),
                    }
                )

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                result,
                file,
                indent=4,
                ensure_ascii=False,
            )

        successful_files = sum(
            1
            for file_data in result["files"]
            if file_data["parse_status"] == "SUCCESS"
        )

        failed_files = (
            len(result["files"])
            - successful_files
        )

        print()
        print(f"Successful parses : {successful_files}")
        print(f"Failed parses     : {failed_files}")
        print(f"Saved             : {output_file}")

        return result

    def _parse_file(
        self,
        file_data: Dict[str, Any],
    ) -> Any:
        """
        Call TreeSitterParser using whichever interface
        the installed parser implementation provides.

        Supported forms:
            parse(file_data)
            parse(source_code, language)
        """

        parse_method = self.parser.parse
        signature = inspect.signature(parse_method)

        # For a bound method, 'self' is not included in the
        # signature parameter count.
        parameter_count = len(signature.parameters)

        if parameter_count == 1:
            return parse_method(file_data)

        if parameter_count == 2:
            return parse_method(
                file_data["source_code"],
                file_data["language"],
            )

        raise TypeError(
            "Unsupported TreeSitterParser.parse() signature. "
            "Expected parse(file) or "
            "parse(source_code, language)."
        )

    def _serialize_result(
        self,
        parsed_result: Any,
    ) -> Dict[str, Any]:
        """
        Convert the parser output into JSON-compatible CST data.

        Supports:
        - A Tree-sitter Tree with root_node
        - A Tree-sitter Node
        - A CST dictionary already serialized by the parser
        """

        if isinstance(parsed_result, dict):
            return parsed_result

        root_node = getattr(
            parsed_result,
            "root_node",
            None,
        )

        if root_node is not None:
            return self.serializer.serialize(
                root_node
            )

        # Some parser implementations may return the root node
        # directly instead of returning a Tree object.
        if hasattr(parsed_result, "type") and hasattr(
            parsed_result,
            "children",
        ):
            return self.serializer.serialize(
                parsed_result
            )

        raise TypeError(
            "TreeSitterParser returned an unsupported result. "
            "Expected a Tree, Node, or serialized CST dictionary."
        )