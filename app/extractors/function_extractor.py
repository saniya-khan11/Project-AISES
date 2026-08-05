from app.ast.function_model import FunctionModel


class FunctionExtractor:
    """
    Extracts functions from a Tree-sitter AST.
    """

    def extract(self, tree, language="Python"):

        functions = []

        self._visit(
            tree.root_node,
            functions,
            language
        )

        return functions

    def _visit(
        self,
        node,
        functions,
        language
    ):

        if node.type == "function_definition":

            function = self._extract_function(
                node,
                language
            )

            functions.append(function)

        for child in node.children:

            self._visit(
                child,
                functions,
                language
            )

    def _extract_function(
        self,
        node,
        language
    ):

        name = ""

        parameters = []

        for child in node.children:

            if child.type == "identifier":

                name = child.text.decode()

            elif child.type == "parameters":

                for parameter in child.children:

                    if parameter.type == "identifier":

                        parameters.append(
                            parameter.text.decode()
                        )

        return FunctionModel(

    name=name,

    language=language,

    parameters=parameters,

    return_type="Unknown",

    start_line=node.start_point[0] + 1,

    end_line=node.end_point[0] + 1,

    source_code="",

    called_functions=[],

    local_variables=[],

    global_variables=[],

    imports=[],

    decorators=[],

    exceptions=[],

    comments=[],

    api_endpoint="",

    http_method="",

    business_intent="",

    matched_requirements=[],

    confidence=0.0,

    semantic_embedding=[],

    ai_summary="",

    recommendation=""
)