import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Окно с меню')
        self.setGeometry(300, 300, 400, 300)

        self.create_menu()

    def create_menu(self):
        exit_action = QAction(QIcon(), 'Exit', self)
        exit_action.setStatusTip('Выход из приложения')
        exit_action.triggered.connect(self.close)

        file_menu = self.menuBar().addMenu('File')
        file_menu.addAction(exit_action)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())