from radon.complexity import cc_rank, cc_visit


class ComplexityCalculator:
    """
    Calculates cyclomatic complexity using Radon.
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
                    "symbol_type": item.__class__.__name__,
                    "cyclomatic_complexity": item.complexity,
                    "rank": cc_rank(item.complexity),
                    "line": item.lineno,
                    "end_line": item.endline,
                    }
                    )

            return complexity

        except Exception:

            return []