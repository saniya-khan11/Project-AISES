class JSONValidator:

    def validate(
        self,
        data,
        required_fields,
    ):

        missing = []

        for field in required_fields:

            if field not in data:

                missing.append(field)

        return missing