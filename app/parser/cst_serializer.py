class CSTSerializer:

    def __init__(self):

        self.node_counter = 1

    def serialize(self, node):

        node_id = f"NODE-{self.node_counter:06d}"

        self.node_counter += 1

        return {

            "node_id": node_id,

            "type": node.type,

            "text": node.text.decode(
                "utf-8",
                errors="ignore"
            ),

            "start_byte": node.start_byte,

            "end_byte": node.end_byte,

            "start_point": {

                "row": node.start_point.row,

                "column": node.start_point.column

            },

            "end_point": {

                "row": node.end_point.row,

                "column": node.end_point.column

            },

            "is_named": node.is_named,

            "children": [

                self.serialize(child)

                for child in node.children

            ]

        }