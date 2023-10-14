import pandas as pd
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QMessageBox
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

        self.label_separation_operations = QLabel('Разделение по ...')

        self.button_separation_date_by_data = QPushButton('... даты от данных')
        self.button_separation_date_by_data.clicked.connect(self.separation_date_by_data)

        self.button_separation_by_years = QPushButton('... годам')
        self.button_separation_by_years.clicked.connect(self.separation_by_years)

        self.button_separation_by_weeks = QPushButton('... неделям')
        self.button_separation_by_weeks.clicked.connect(self.separation_by_weeks)

        v_layout.addWidget(self.button_choose_dataset)
        v_layout.addWidget(self.textbox_date)
        v_layout.addWidget(self.button_search)

        v_layout.addWidget(self.label_separation_operations)
        v_layout.addWidget(self.button_separation_date_by_data)
        v_layout.addWidget(self.button_separation_by_years)
        v_layout.addWidget(self.button_separation_by_weeks)

        
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
        #print(dataset_operations.get_data_from_date(self.df, date_datetime))

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(str(dataset_operations.get_data_from_date(self.df, date_datetime)))
        msg.setWindowTitle("Полученные данные по дате")
        msg.exec()
    
    #пофиксить баг с датой
    def separation_date_by_data(self):
        dataset_operations = DatasetOperations(self.folder_path)
        dataset_operations.separation_date_by_data(self.df)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText('Данные отделены от даты')
        msg.setWindowTitle("Данные от даты")
        msg.exec()

    def separation_by_years(self):
        dataset_operations = DatasetOperations(self.folder_path)
        dataset_operations.separation_by_years(self.df)   

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText('Данные разделены по годам')
        msg.setWindowTitle("Разделение по годам")
        msg.exec()

    def separation_by_weeks(self):
        dataset_operations = DatasetOperations(self.folder_path)
        dataset_operations.separation_by_weeks(self.df)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText('Данные разделены по неделям')
        msg.setWindowTitle("Разделение по неделям")
        msg.exec()

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