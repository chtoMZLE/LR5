import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QColor


class ColorChanger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Окно')

        self.color = QColor(0, 0, 0)

        button = QPushButton('Смена цвета', self)
        button.setCheckable(True)
        button.move(10, 10)
        button.clicked.connect(self.change_color)

        self.square = QWidget(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet(f"background-color: {self.color.name()};")

    def change_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        self.square.setStyleSheet(f"background-color: rgb({red}, {green}, {blue});")


app = QApplication(sys.argv)
window = ColorChanger()
window.show()
sys.exit(app.exec_())