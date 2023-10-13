from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit
from PyQt6.QtCore import QDate

from dataset_handler import DatasetHandler
from operations_dataset import DatasetOperations
from datetime import datetime

dat_h = DatasetHandler()
CURRENCY_FIELDS = ['date', 'nominal', 'value', 'vunitRate']

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operations with datasets")

        self.file_path = ""
        self.df = ""

        layout = QVBoxLayout()

        self.button = QPushButton("Выбор датасета")
        self.button.clicked.connect(self.pick_file)

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Введите дату")

        self.search_button = QPushButton("Найти")
        self.search_button.clicked.connect(self.search_date)

        layout.addWidget(self.button)
        layout.addWidget(self.date_input)
        layout.addWidget(self.search_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.pick_file()


    def pick_file(self):
        file_dialog = QFileDialog()
        self.file_path = file_dialog.getOpenFileName()[0]
        print(self.file_path)
        self.df = dat_h.create_dataset_from_files([self.file_path], CURRENCY_FIELDS)

    def search_date(self):
        date_str = self.date_input.text()
        date = QDate.fromString(date_str, "dd.MM.yyyy")
        date_datetime = datetime(date.year(), date.month(), date.day())
        dataset_operations = DatasetOperations(self.file_path)
        print(dataset_operations.get_data_from_date(self.df, date_datetime))


app = QApplication([])
window = MainWindow()
window.show()

app.exec()