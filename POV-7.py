import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class SQLiteBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = None
        self.current_table = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SQLite Browser")
        self.setGeometry(100, 100, 1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        toolbar = QHBoxLayout()

        open_btn = QPushButton("Открыть базу")
        open_btn.clicked.connect(self.open_database)

        new_btn = QPushButton("Новая база")
        new_btn.clicked.connect(self.new_database)

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.save_changes)
        self.save_button = save_btn
        save_btn.setEnabled(False)

        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.refresh_data)
        self.refresh_button = refresh_btn
        refresh_btn.setEnabled(False)

        toolbar.addWidget(open_btn)
        toolbar.addWidget(new_btn)
        toolbar.addWidget(save_btn)
        toolbar.addWidget(refresh_btn)

        main_layout.addLayout(toolbar)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        left_layout.addWidget(QLabel("Таблицы:"))

        self.tables_list = QListWidget()
        self.tables_list.itemClicked.connect(self.show_table)
        left_layout.addWidget(self.tables_list)

        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("Таблица:"))
        self.table_name_label = QLabel("Не выбрано")
        info_layout.addWidget(self.table_name_label)
        info_layout.addStretch()

        right_layout.addLayout(info_layout)

        self.data_table = QTableWidget()
        self.data_table.itemChanged.connect(self.data_changed)
        right_layout.addWidget(self.data_table)

        splitter.addWidget(right_widget)

        splitter.setSizes([200, 800])
        main_layout.addWidget(splitter)

        sql_widget = QWidget()
        sql_layout = QVBoxLayout(sql_widget)

        sql_layout.addWidget(QLabel("SQL запрос:"))

        self.sql_input = QTextEdit()
        self.sql_input.setPlaceholderText("Введите SQL запрос...")
        sql_layout.addWidget(self.sql_input)

        sql_buttons = QHBoxLayout()

        run_sql_btn = QPushButton("Выполнить")
        run_sql_btn.clicked.connect(self.run_sql)
        self.run_sql_button = run_sql_btn
        run_sql_btn.setEnabled(False)

        clear_sql_btn = QPushButton("Очистить")
        clear_sql_btn.clicked.connect(self.clear_sql)

        sql_buttons.addWidget(run_sql_btn)
        sql_buttons.addWidget(clear_sql_btn)
        sql_buttons.addStretch()

        sql_layout.addLayout(sql_buttons)

        sql_layout.addWidget(QLabel("Результат:"))

        self.sql_result_table = QTableWidget()
        sql_layout.addWidget(self.sql_result_table)

        self.sql_status = QLabel("Готово")
        sql_layout.addWidget(self.sql_status)

        main_layout.addWidget(QLabel("SQL запросы:"))
        main_layout.addWidget(sql_widget)

        self.status_bar = QLabel("Откройте базу данных")
        self.status_bar.setStyleSheet("background: #e0e0e0; padding: 5px;")
        main_layout.addWidget(self.status_bar)

    def open_database(self):
        file_name = QFileDialog.getOpenFileName(
            self, "Открыть базу",
            "", "Базы данных (*.db *.sqlite)"
        )[0]

        if file_name:
            try:
                if self.connection:
                    self.connection.close()

                self.connection = sqlite3.connect(file_name)

                db_name = file_name.split('/')[-1]
                self.setWindowTitle(f"SQLite Browser - {db_name}")

                self.load_tables()

                self.save_button.setEnabled(True)
                self.refresh_button.setEnabled(True)
                self.run_sql_button.setEnabled(True)

                self.status_bar.setText(f"Открыта база: {db_name}")

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Нельзя открыть базу:\n{e}")

    def new_database(self):
        file_name = QFileDialog.getSaveFileName(
            self, "Создать базу",
            "", "Базы данных (*.db)"
        )[0]

        if file_name:
            try:
                if self.connection:
                    self.connection.close()

                self.connection = sqlite3.connect(file_name)

                db_name = file_name.split('/')[-1]
                self.setWindowTitle(f"SQLite Browser - {db_name}")

                self.tables_list.clear()
                self.data_table.setRowCount(0)
                self.data_table.setColumnCount(0)
                self.table_name_label.setText("Не выбрано")
                self.sql_result_table.setRowCount(0)
                self.sql_result_table.setColumnCount(0)

                self.save_button.setEnabled(True)
                self.refresh_button.setEnabled(True)
                self.run_sql_button.setEnabled(True)

                self.status_bar.setText(f"Создана база: {db_name}")

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Нельзя создать базу:\n{e}")

    def load_tables(self):
        if not self.connection:
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = cursor.fetchall()

            self.tables_list.clear()

            for table in tables:
                self.tables_list.addItem(table[0])

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не загрузить таблицы:\n{e}")

    def show_table(self, item):
        table_name = item.text()
        self.current_table = table_name
        self.table_name_label.setText(table_name)

        if not self.connection:
            return

        try:
            self.load_table_data(table_name)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Нельзя загрузить данные:\n{e}")

    def load_table_data(self, table_name):
        if not self.connection:
            return

        cursor = self.connection.cursor()

        cursor.execute(f"SELECT * FROM '{table_name}'")
        data = cursor.fetchall()

        cursor.execute(f"PRAGMA table_info('{table_name}')")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]

        self.data_table.setRowCount(len(data))
        self.data_table.setColumnCount(len(column_names))
        self.data_table.setHorizontalHeaderLabels(column_names)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data) if cell_data is not None else "")
                self.data_table.setItem(row_idx, col_idx, item)

        self.status_bar.setText(f"Загружено {len(data)} записей из {table_name}")

    def data_changed(self, item):
        if not self.connection or not self.current_table:
            return

        self.save_button.setStyleSheet("background-color: yellow")
        self.status_bar.setText("Есть несохраненные изменения")

    def save_changes(self):
        if not self.connection or not self.current_table:
            return

        try:
            cursor = self.connection.cursor()

            cursor.execute(f"PRAGMA table_info('{self.current_table}')")
            columns_info = cursor.fetchall()
            column_names = [col[1] for col in columns_info]

            self.connection.execute("BEGIN TRANSACTION")

            cursor.execute(f"DELETE FROM '{self.current_table}'")

            for row in range(self.data_table.rowCount()):
                row_data = []

                for col in range(self.data_table.columnCount()):
                    item = self.data_table.item(row, col)
                    value = item.text() if item else ""

                    if value == "":
                        row_data.append(None)
                    else:
                        row_data.append(value)

                placeholders = ", ".join(["?" for _ in column_names])
                insert_sql = f"INSERT INTO '{self.current_table}' VALUES ({placeholders})"

                cursor.execute(insert_sql, row_data)

            self.connection.commit()

            self.save_button.setStyleSheet("")
            self.status_bar.setText("Изменения сохранены")

        except Exception as e:
            self.connection.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не сохранить:\n{e}")

    def run_sql(self):
        if not self.connection:
            return

        sql = self.sql_input.toPlainText().strip()

        if not sql:
            QMessageBox.warning(self, "Внимание", "Введите SQL запрос")
            return

        self.sql_result_table.setRowCount(0)
        self.sql_result_table.setColumnCount(0)

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)

            if sql.strip().upper().startswith("SELECT"):
                data = cursor.fetchall()

                if cursor.description:
                    column_names = [desc[0] for desc in cursor.description]

                    self.sql_result_table.setRowCount(len(data))
                    self.sql_result_table.setColumnCount(len(column_names))
                    self.sql_result_table.setHorizontalHeaderLabels(column_names)

                    for row_idx, row_data in enumerate(data):
                        for col_idx, cell_data in enumerate(row_data):
                            item = QTableWidgetItem(str(cell_data) if cell_data is not None else "")
                            self.sql_result_table.setItem(row_idx, col_idx, item)

                    self.sql_status.setText(f"Найдено {len(data)} записей")
                else:
                    self.sql_status.setText("Нет данных")

            else:
                self.connection.commit()
                rows = cursor.rowcount

                self.load_tables()

                if self.current_table:
                    self.load_table_data(self.current_table)

                self.sql_status.setText(f"Выполнено. Затронуто строк: {rows}")

        except Exception as e:
            self.sql_status.setText(f"Ошибка: {str(e)[:50]}...")
            QMessageBox.critical(self, "Ошибка SQL", f"Не выполнить запрос:\n{e}")

    def clear_sql(self):
        self.sql_input.clear()
        self.sql_result_table.setRowCount(0)
        self.sql_result_table.setColumnCount(0)
        self.sql_status.setText("Готово")

    def refresh_data(self):
        if self.current_table:
            self.load_table_data(self.current_table)
            self.status_bar.setText("Данные обновлены")

    def closeEvent(self, event):
        if self.connection:
            self.connection.close()
        event.accept()


app = QApplication(sys.argv)

window = SQLiteBrowser()
window.show()

sys.exit(app.exec_())