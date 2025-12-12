import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.current_input = "0"
        self.first_number = None
        self.current_operator = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.display_label = QLabel("0")
        self.display_label.setFixedHeight(50)
        main_layout.addWidget(self.display_label)

        buttons = [
            ['7', '8', '9', '+'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '*'],
            ['0', 'C', '=', '/']
        ]

        for row_buttons in buttons:
            row_layout = QHBoxLayout()

            for button_text in row_buttons:
                button = QPushButton(button_text)
                button.clicked.connect(lambda checked, text=button_text: self.on_button_click(text))
                row_layout.addWidget(button)

            main_layout.addLayout(row_layout)

        self.setLayout(main_layout)

        self.setWindowTitle("Калькулятор")
        self.setFixedSize(300, 300)

    def on_button_click(self, button_text):
        if button_text == 'C':
            self.clear_calculator()

        elif button_text == '=':
            self.calculate_result()

        elif button_text in '+-*/':
            self.handle_operator(button_text)

        else:
            self.handle_digit(button_text)

    def clear_calculator(self):
        self.current_input = "0"
        self.first_number = None
        self.current_operator = None
        self.display_label.setText("0")

    def calculate_result(self):
        if self.first_number is not None and self.current_operator and self.current_input != "0":
            result = eval(f"{self.first_number}{self.current_operator}{self.current_input}")

            self.display_label.setText(str(result))

            self.current_input = str(result)

            self.first_number = None
            self.current_operator = None


    def handle_operator(self, operator):
        if self.current_input != "0":
            self.first_number = self.current_input
            self.current_operator = operator
            self.current_input = "0"

    def handle_digit(self, digit):
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit

        self.display_label.setText(self.current_input)


app = QApplication(sys.argv)
calculator = Calculator()
calculator.show()
sys.exit(app.exec_())