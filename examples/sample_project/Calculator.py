import tkinter as tk
from tkinter import ttk
class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")

        self.first = 0.0
        self.operator = None
        self.new_input = True
        self.display = tk.StringVar(value="0")

        ttk.Entry(
            root,
            textvariable=self.display,
            justify="right",
            state="readonly",
            font=("Arial", 20),
            width=18,
        ).grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        button_data = [
            ("C", self.clear), ("DEL", self.delete),
            ("7", lambda: self.digit("7")), ("8", lambda: self.digit("8")),
            ("9", lambda: self.digit("9")), ("/", lambda: self.set_operator("/")),
            ("4", lambda: self.digit("4")), ("5", lambda: self.digit("5")),
            ("6", lambda: self.digit("6")), ("*", lambda: self.set_operator("*")),
            ("1", lambda: self.digit("1")), ("2", lambda: self.digit("2")),
            ("3", lambda: self.digit("3")), ("-", lambda: self.set_operator("-")),
            (".", self.decimal), ("0", lambda: self.digit("0")),
            ("=", self.calculate), ("+", lambda: self.set_operator("+")),
        ]

        for index, (text, command) in enumerate(button_data):
            row = 1 + index // 4
            column = index % 4

            ttk.Button(
                root,
                text=text,
                command=command,
                width=7,
            ).grid(row=row, column=column, padx=4, pady=4)

    def digit(self, value):
        current = self.display.get()

        if self.new_input or current == "0":
            self.display.set(value)
            self.new_input = False
        else:
            self.display.set(current + value)

    def decimal(self):
        current = self.display.get()

        if self.new_input:
            self.display.set("0.")
            self.new_input = False
        elif "." not in current:
            self.display.set(current + ".")

    def set_operator(self, operator):
        try:
            self.first = float(self.display.get())
            self.operator = operator
            self.new_input = True
        except ValueError:
            self.clear()

    def clear(self):
        self.display.set("0")
        self.first = 0.0
        self.operator = None
        self.new_input = True

    def delete(self):
        current = self.display.get()

        if len(current) > 1:
            self.display.set(current[:-1])
        else:
            self.display.set("0")
            self.new_input = True

    def calculate(self):
        if self.operator is None:
            return

        try:
            second = float(self.display.get())

            operations = {
                "+": lambda: self.first + second,
                "-": lambda: self.first - second,
                "*": lambda: self.first * second,
                "/": lambda: self.first / second,
            }

            result = operations[self.operator]()
            self.display.set(
                str(int(result)) if result.is_integer() else str(result)
            )

            self.first = result
            self.operator = None
            self.new_input = True

        except Exception:
            self.display.set("Error")
            self.operator = None
            self.new_input = True


root = tk.Tk()
Calculator(root)
root.mainloop()