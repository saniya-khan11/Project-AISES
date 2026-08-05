class CallGraphExtractor:
    """
    Extracts function calls from a Tree-sitter AST.
    """

    def extract(self, tree, functions):

        self.functions = functions

        self._visit(tree.root_node)

        return functions

    def _visit(self, node):

        if node.type == "call":

            function_name = None

            for child in node.children:

                if child.type == "identifier":

                    function_name = child.text.decode()

                    break

            if function_name:

                self._assign_call(
                    node,
                    function_name
                )

        for child in node.children:

            self._visit(child)

    def _assign_call(
        self,
        call_node,
        function_name,
    ):

        line = call_node.start_point[0] + 1

        for function in self.functions:

            if function.start_line <= line <= function.end_line:

                if function_name not in function.called_functions:

                    function.called_functions.append(
                        function_name
                    )

                break