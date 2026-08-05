from typing import Any, Dict

import tree_sitter_python
from tree_sitter import Language, Parser


class TreeSitterParser:
    """
    Tree-sitter parser for Python source code.

    Uses the dedicated tree-sitter-python package so it works
    on Windows without downloading parsers at runtime.
    """

    def __init__(self) -> None:
        python_language = Language(
            tree_sitter_python.language()
        )

        try:
            self.parser = Parser(python_language)
        except TypeError:
            self.parser = Parser()
            self.parser.language = python_language

    def parse(
        self,
        source_code: str,
        language: str,
    ) -> Dict[str, Any]:
        normalized_language = str(language).strip().lower()

        if normalized_language != "python":
            raise ValueError(
                f"Unsupported language: {language}"
            )

        if not isinstance(source_code, str):
            raise TypeError(
                "source_code must be a string."
            )

        source_bytes = source_code.encode("utf-8")
        tree = self.parser.parse(source_bytes)

        return self._node_to_dict(
            tree.root_node,
            source_bytes,
        )

    def _node_to_dict(
        self,
        node,
        source_bytes: bytes,
    ) -> Dict[str, Any]:
        text = source_bytes[
            node.start_byte:node.end_byte
        ].decode(
            "utf-8",
            errors="replace",
        )

        return {
            "type": node.type,
            "text": text,
            "start_byte": node.start_byte,
            "end_byte": node.end_byte,
            "start_point": {
                "row": node.start_point.row,
                "column": node.start_point.column,
            },
            "end_point": {
                "row": node.end_point.row,
                "column": node.end_point.column,
            },
            "is_named": node.is_named,
            "has_error": node.has_error,
            "children": [
                self._node_to_dict(
                    child,
                    source_bytes,
                )
                for child in node.children
            ],
        }