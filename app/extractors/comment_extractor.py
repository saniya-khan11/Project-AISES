class CommentExtractor:
    """
    Extracts comments associated with functions.
    Supports Python comments (#) for now.
    """

    def extract(self, source_code, functions):

        lines = source_code.splitlines()

        for function in functions:

            comments = []

            # Look up to 3 lines above the function
            start = max(0, function.start_line - 4)
            end = function.start_line - 1

            for i in range(start, end):

                line = lines[i].strip()

                if line.startswith("#"):

                    comments.append(
                        line.lstrip("#").strip()
                    )

            function.comments = comments

        return functions