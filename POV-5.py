import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont


class TimerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.stopwatch_running = False
        self.stopwatch_time = 0

        self.timer_running = False
        self.timer_time = 0
        self.timer_total = 0

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_time)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Часы")
        self.setFixedSize(400, 400)

        tabs = QTabWidget()

        stopwatch_tab = QWidget()
        stopwatch_layout = QVBoxLayout()

        self.stopwatch_display = QLabel("00:00:00.000")
        stopwatch_font = QFont("Arial", 32)
        self.stopwatch_display.setFont(stopwatch_font)
        self.stopwatch_display.setAlignment(Qt.AlignCenter)
        stopwatch_layout.addWidget(self.stopwatch_display)

        stopwatch_buttons_layout = QHBoxLayout()

        self.stopwatch_start_button = QPushButton("Старт")
        self.stopwatch_start_button.clicked.connect(self.start_stopwatch)
        stopwatch_buttons_layout.addWidget(self.stopwatch_start_button)

        self.stopwatch_pause_button = QPushButton("Пауза")
        self.stopwatch_pause_button.clicked.connect(self.pause_stopwatch)
        stopwatch_buttons_layout.addWidget(self.stopwatch_pause_button)

        self.stopwatch_reset_button = QPushButton("Сброс")
        self.stopwatch_reset_button.clicked.connect(self.reset_stopwatch)
        stopwatch_buttons_layout.addWidget(self.stopwatch_reset_button)

        stopwatch_layout.addLayout(stopwatch_buttons_layout)

        stopwatch_tab.setLayout(stopwatch_layout)

        timer_tab = QWidget()
        timer_layout = QVBoxLayout()

        self.timer_display = QLabel("00:00:00")
        timer_font = QFont("Arial", 32)
        self.timer_display.setFont(timer_font)
        self.timer_display.setAlignment(Qt.AlignCenter)
        timer_layout.addWidget(self.timer_display)

        time_input_layout = QGridLayout()

        time_input_layout.addWidget(QLabel("Часы:"), 0, 0)
        self.timer_hours_input = QSpinBox()
        self.timer_hours_input.setRange(0, 23)
        self.timer_hours_input.setValue(0)
        time_input_layout.addWidget(self.timer_hours_input, 0, 1)

        time_input_layout.addWidget(QLabel("Минуты:"), 1, 0)
        self.timer_minutes_input = QSpinBox()
        self.timer_minutes_input.setRange(0, 59)
        self.timer_minutes_input.setValue(0)
        time_input_layout.addWidget(self.timer_minutes_input, 1, 1)

        time_input_layout.addWidget(QLabel("Секунды:"), 2, 0)
        self.timer_seconds_input = QSpinBox()
        self.timer_seconds_input.setRange(0, 59)
        self.timer_seconds_input.setValue(0)
        time_input_layout.addWidget(self.timer_seconds_input, 2, 1)

        timer_layout.addLayout(time_input_layout)

        timer_buttons_layout = QHBoxLayout()

        self.timer_start_button = QPushButton("Старт")
        self.timer_start_button.clicked.connect(self.start_timer)
        timer_buttons_layout.addWidget(self.timer_start_button)

        self.timer_pause_button = QPushButton("Пауза")
        self.timer_pause_button.clicked.connect(self.pause_timer)
        timer_buttons_layout.addWidget(self.timer_pause_button)

        self.timer_reset_button = QPushButton("Сброс")
        self.timer_reset_button.clicked.connect(self.reset_timer)
        timer_buttons_layout.addWidget(self.timer_reset_button)

        timer_layout.addLayout(timer_buttons_layout)

        timer_tab.setLayout(timer_layout)

        tabs.addTab(stopwatch_tab, "Секундомер")
        tabs.addTab(timer_tab, "Таймер")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)

        self.setLayout(main_layout)

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.update_timer.start(10)  # Обновление каждые 10 мс
            self.stopwatch_start_button.setEnabled(False)
            self.stopwatch_pause_button.setEnabled(True)

    def pause_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_running = False
            self.update_timer.stop()
            self.stopwatch_start_button.setEnabled(True)
            self.stopwatch_pause_button.setEnabled(False)

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.update_timer.stop()
        self.stopwatch_time = 0
        self.stopwatch_display.setText("00:00:00.000")
        self.stopwatch_start_button.setEnabled(True)
        self.stopwatch_pause_button.setEnabled(False)

    def start_timer(self):
        if not self.timer_running:
            if self.timer_time == 0:
                hours = self.timer_hours_input.value()
                minutes = self.timer_minutes_input.value()
                seconds = self.timer_seconds_input.value()

                if hours == 0 and minutes == 0 and seconds == 0:
                    QMessageBox.warning(self, "Внимание", "Установите время для таймера")
                    return

                self.timer_time = (hours * 3600 + minutes * 60 + seconds) * 1000
                self.timer_total = self.timer_time

            self.timer_running = True
            self.update_timer.start(10)  # Обновление каждые 10 мс
            self.timer_start_button.setEnabled(False)
            self.timer_pause_button.setEnabled(True)

    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.update_timer.stop()
            self.timer_start_button.setEnabled(True)
            self.timer_pause_button.setEnabled(False)

    def reset_timer(self):
        self.timer_running = False
        self.update_timer.stop()
        self.timer_time = 0
        self.timer_total = 0
        self.timer_display.setText("00:00:00")
        self.timer_hours_input.setValue(0)
        self.timer_minutes_input.setValue(0)
        self.timer_seconds_input.setValue(0)
        self.timer_start_button.setEnabled(True)
        self.timer_pause_button.setEnabled(False)

    def update_time(self):
        if self.stopwatch_running:
            self.stopwatch_time += 10  # Увеличиваем на 10 мс
            self.update_stopwatch_display()

        elif self.timer_running and self.timer_time > 0:
            self.timer_time -= 10  # Уменьшаем на 10 мс

            self.update_timer_display()

            if self.timer_time <= 0:
                self.timer_finished()

    def timer_finished(self):
        self.timer_running = False
        self.update_timer.stop()
        self.timer_time = 0
        self.timer_display.setText("00:00:00")

        QMessageBox.information(self, "Таймер", "Время вышло!")

        self.timer_start_button.setEnabled(False)
        self.timer_pause_button.setEnabled(False)

    def update_stopwatch_display(self):
        time_str = self.format_stopwatch_time(self.stopwatch_time)
        self.stopwatch_display.setText(time_str)

    def update_timer_display(self):
        time_str = self.format_timer_time(self.timer_time)
        self.timer_display.setText(time_str)

    def format_stopwatch_time(self, milliseconds):
        hours = int(milliseconds // 3600000)
        minutes = int((milliseconds % 3600000) // 60000)
        seconds = int((milliseconds % 60000) // 1000)
        ms = int(milliseconds % 1000)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{ms:03d}"

    def format_timer_time(self, milliseconds):
        total_seconds = int(milliseconds // 1000)
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"


app = QApplication(sys.argv)

window = TimerApp()
window.show()

sys.exit(app.exec_())