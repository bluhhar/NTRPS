import pandas as pd
import datetime

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt6.QtCore import QDate

from dataset_handler import DatasetHandler
from operations_dataset import DatasetOperations

dat_h = DatasetHandler()
CURRENCY_FIELDS = ['date', 'nominal', 'value', 'vunitRate']

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Operations with datasets')

        self.folder_path = ""
        self.df = pd.DataFrame()

        v_layout = QVBoxLayout()

        self.button_choose_dataset = QPushButton('Выбор датасета')
        self.button_choose_dataset.clicked.connect(self.choose_dataset_from_file)

        self.textbox_date = QLineEdit()
        self.textbox_date.setPlaceholderText('Введите дату')

        self.button_search = QPushButton('Получить данные')
        self.button_search.clicked.connect(self.get_data_with_date)

        v_layout.addWidget(self.button_choose_dataset)
        v_layout.addWidget(self.textbox_date)
        v_layout.addWidget(self.button_search)

        
        v_layout.addStretch(1) #чтобы кнопки не расплылись по форме от горизонтального слоя

        self.table = QTableWidget()
        
        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)
        h_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(h_layout)

        self.setCentralWidget(container)

        self.choose_dataset_from_file()


    def choose_dataset_from_file(self):
        file_dialog = QFileDialog()
        self.folder_path = file_dialog.getOpenFileName()[0]
        print(self.folder_path)
        self.df = dat_h.create_dataset_from_files([self.folder_path], CURRENCY_FIELDS)
        self.update_table()

    def get_data_with_date(self):
        date_str = self.textbox_date.text()
        date = QDate.fromString(date_str, 'dd.MM.yyyy')
        date_datetime = datetime(date.year(), date.month(), date.day())
        dataset_operations = DatasetOperations(self.folder_path)
        print(dataset_operations.get_data_from_date(self.df, date_datetime))

    def update_table(self):
        if not self.df.empty:
            self.table.setRowCount(len(self.df))
            self.table.setColumnCount(len(self.df.columns))
            self.table.setHorizontalHeaderLabels(self.df.columns)
            for i in range(len(self.df)):
                for j in range(len(self.df.columns)):
                    self.table.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))
            self.table.resizeColumnsToContents()


def main():
    app = QApplication([])
    window = MainWindow()
    window.setMinimumWidth(700)
    window.setMinimumHeight(700)
    window.show()

    app.exec()

if __name__ == '__main__':
    main()