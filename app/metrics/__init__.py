from radon.complexity import cc_visit


class ComplexityCalculator:
    """
    Purpose:
        Calculates cyclomatic complexity for Python source code.

    Responsibilities:
        - Parse source code using Radon.
        - Return structured complexity metrics.

    Output:
        List[dict]
    """

    def calculate(self, source_code):

        if not source_code:
            return []

        try:

            results = cc_visit(source_code)

            complexity = []

            for item in results:

                complexity.append(
                    {
                        "name": item.name,
                        "type": item.__class__.__name__,
                        "complexity": item.complexity,
                        "line": item.lineno,
                        "end_line": item.endline,
                    }
                )

            return complexity

        except Exception:

            return []