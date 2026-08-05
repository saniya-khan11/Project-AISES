class VariableExtractor:
    """
    Extracts local variables from a Tree-sitter AST.
    """

    def extract(self, tree, functions):

        self.functions = functions

        self._visit(tree.root_node)

        return functions

    def _visit(self, node):

        # Python assignment
        if node.type == "assignment":

            variable_name = None

            for child in node.children:

                if child.type == "identifier":

                    variable_name = child.text.decode()

                    break

            if variable_name:

                self._assign_variable(
                    node,
                    variable_name
                )

        for child in node.children:

            self._visit(child)

    def _assign_variable(
        self,
        assignment_node,
        variable_name,
    ):

        line = assignment_node.start_point[0] + 1

        for function in self.functions:

            if function.start_line <= line <= function.end_line:

                if variable_name not in function.local_variables:

                    function.local_variables.append(
                        variable_name
                    )

                break