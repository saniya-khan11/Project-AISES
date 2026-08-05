from app.ast.class_model import ClassModel


class ClassExtractor:
    """
    Extracts classes from a Tree-sitter AST.
    """

    def extract(self, tree, language="Python"):

        classes = []

        self._visit(
            tree.root_node,
            classes,
            language
        )

        return classes

    def _visit(
        self,
        node,
        classes,
        language
    ):

        if node.type == "class_definition":

            classes.append(
                self._extract_class(
                    node,
                    language
                )
            )

        for child in node.children:

            self._visit(
                child,
                classes,
                language
            )

    def _extract_class(
        self,
        node,
        language
    ):

        name = ""

        methods = []

        for child in node.children:

            if child.type == "identifier":

                name = child.text.decode()

            elif child.type == "block":

                for item in child.children:

                    if item.type == "function_definition":

                        for x in item.children:

                            if x.type == "identifier":

                                methods.append(
                                    x.text.decode()
                                )

        return ClassModel(

            name=name,

            language=language,

            methods=methods,

            start_line=node.start_point[0] + 1,

            end_line=node.end_point[0] + 1,
        )