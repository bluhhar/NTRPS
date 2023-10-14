import pandas as pd
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QMessageBox, QComboBox
from PyQt6.QtCore import QDate

from dataset_handler import DatasetHandler
from operations_dataset import DatasetOperations
from directory_handler import DirectoryHandler as dir_h

from form_images import ImageWindow

dat_h = DatasetHandler()
CURRENCY_FIELDS = ['date', 'nominal', 'value', 'vunitRate']
IMAGES_FIELDS = ['date', 'file_name', 'url', 'path']

CURR_DIR = dir_h.set_current_dir()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Operations with datasets')

        self.folder_path = ""
        self.df = pd.DataFrame()

        self.dataset_operations = DatasetOperations(CURR_DIR)

        v_layout = QVBoxLayout()

        self.button_choose_dataset = QPushButton('Выбор датасета')
        self.button_choose_dataset.clicked.connect(self.choose_dataset_from_file)

        self.combo_box_fields = QComboBox()
        self.combo_box_fields.addItem("'date', 'nominal', 'value', 'vunitRate'")
        self.combo_box_fields.addItem("'date', 'file_name', 'url', 'path'")

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

        self.button_show_images = QPushButton('Просмотр картинок')
        self.button_show_images.clicked.connect(self.show_form_images)

        v_layout.addWidget(self.button_choose_dataset)
        v_layout.addWidget(self.combo_box_fields)
        v_layout.addWidget(self.textbox_date)
        v_layout.addWidget(self.button_search)

        v_layout.addWidget(self.label_separation_operations)
        v_layout.addWidget(self.button_separation_date_by_data)
        v_layout.addWidget(self.button_separation_by_years)
        v_layout.addWidget(self.button_separation_by_weeks)
        v_layout.addWidget(self.button_show_images)

        
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
        self.df = dat_h.create_dataset_from_files([self.folder_path], CURRENCY_FIELDS)#self.combo_box_fields.currentText())#CURRENCY_FIELDS)
        self.update_table()

    def show_message_box(self, title, text):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setText(text)
        message_box.setWindowTitle(title)
        message_box.exec()

    def get_data_with_date(self):
        date_str = self.textbox_date.text()
        date = QDate.fromString(date_str, 'dd.MM.yyyy')
        date_datetime = datetime(date.year(), date.month(), date.day())
        data = self.dataset_operations.get_data_from_date(self.df, date_datetime)
        self.show_message_box("Полученные данные по дате", str(data))

    def separation_date_by_data(self):
        self.dataset_operations.separation_date_by_data(self.df)
        self.show_message_box("Данные от даты", 'Данные отделены от даты')

    def separation_by_years(self):
        self.dataset_operations.separation_by_years(self.df)   
        self.show_message_box("Разделение по годам", 'Данные разделены по годам')

    def separation_by_weeks(self):
        self.dataset_operations.separation_by_weeks(self.df)
        self.show_message_box("Разделение по неделям", 'Данные разделены по неделям')

    def update_table(self):
        if not self.df.empty:
            self.table.setRowCount(len(self.df))
            self.table.setColumnCount(len(self.df.columns))
            self.table.setHorizontalHeaderLabels(self.df.columns)
            for i in range(len(self.df)):
                for j in range(len(self.df.columns)):
                    item = self.df.iat[i, j]
                    if j == 0: #'date'
                        date_str = item.strftime('%Y-%m-%d')
                        date = QDate.fromString(date_str, 'yyyy-MM-dd')
                        item_str = date.toString('yyyy-MM-dd')
                    else:
                        item_str = str(item)
                    self.table.setItem(i, j, QTableWidgetItem(item_str))
                    #self.table.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))
            self.table.resizeColumnsToContents()

    def show_form_images(self):
        self.image_window = ImageWindow(self.df)
        self.image_window.show()

def check_repos():
    dir_h.check_repository(CURR_DIR, 'datasets')
    dir_h.check_repository(CURR_DIR, 'csv')
    dir_h.check_repository(CURR_DIR, 'csv/csv_date_by_data')
    dir_h.check_repository(CURR_DIR, 'csv/csv_years')
    dir_h.check_repository(CURR_DIR, 'csv/csv_weeks')
    dir_h.check_repository(CURR_DIR, 'datasets/images')
    dir_h.check_repository(CURR_DIR, 'datasets/currency')

def main():
    check_repos()
    app = QApplication([])
    window = MainWindow()
    window.setMinimumWidth(700)
    window.setMinimumHeight(700)
    window.show()

    app.exec()

if __name__ == '__main__':
    main()