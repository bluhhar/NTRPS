import pandas as pd

from datetime import datetime

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QMessageBox, QComboBox
from PyQt6.QtCore import QDate

from dataset_handler import DatasetHandler
from operations_dataset import DatasetOperations
from directory_handler import DirectoryHandler as dir_h

from form_images import ImageWindow
from form_currency import CurrencyWindow
from form_choose_date import PlotChooseDateForm

CURRENCY_FIELDS = ['date', 'nominal', 'value', 'vunitRate']
IMAGES_FIELDS = ['date', 'file_name', 'url', 'path']

CURR_DIR = dir_h.set_current_dir()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folder_path = ""
        self.df = pd.DataFrame()

        self.dataset_operations = DatasetOperations(CURR_DIR)
        
        self.is_loaded_dataset = False
        self.is_nan_check = False
        self.is_rename_columns = False
        self.is_add_median_mean = False

        self.init_ui()
        self.choose_dataset_from_file()


    def init_ui(self):
        self.setWindowTitle('Операции с датасетом')
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

        self.button_show_images = QPushButton('Просмотр данных')
        self.button_show_images.clicked.connect(self.show_form_data)

        v_layout.addWidget(self.button_choose_dataset)
        v_layout.addWidget(self.combo_box_fields)
        v_layout.addWidget(self.textbox_date)
        v_layout.addWidget(self.button_search)

        v_layout.addWidget(self.label_separation_operations)
        v_layout.addWidget(self.button_separation_date_by_data)
        v_layout.addWidget(self.button_separation_by_years)
        v_layout.addWidget(self.button_separation_by_weeks)
        v_layout.addWidget(self.button_show_images)
        
        self.label_info_dataset = QLabel('Информация о датасете')

        self.button_info_of_dataset = QPushButton('Информация')
        self.button_info_of_dataset.clicked.connect(self.info_of_dataset)

        self.button_rename_columns = QPushButton('Переименовать колонки')
        self.button_rename_columns.clicked.connect(self.rename_columns)

        self.button_check_null_fields = QPushButton('Проверка на NaN')
        self.button_check_null_fields.clicked.connect(self.check_null_fields)
        self.button_check_null_fields.setEnabled(False)
        
        self.button_median_mean = QPushButton('Медианы и средний')
        self.button_median_mean.clicked.connect(self.median_mean)
        self.button_median_mean.setEnabled(False)

        self.button_describe_dataset = QPushButton('Статистическая информация')
        self.button_describe_dataset.clicked.connect(self.describe_dataset)
        self.button_describe_dataset.setEnabled(False)

        self.label_graphs = QLabel('Графики датасета')

        self.button_show_deviation_graph = QPushButton('График отклонения')
        self.button_show_deviation_graph.clicked.connect(self.show_deviation_graph)
        self.button_show_deviation_graph.setEnabled(False)

        self.button_show_date_graph = QPushButton('График изменения курса')
        self.button_show_date_graph.clicked.connect(self.show_date_graph)
        self.button_show_date_graph.setEnabled(False)

        self.textbox_date_graph = QLineEdit()
        self.textbox_date_graph.setPlaceholderText('Введите дату (<месяц> ИЛИ <год> ИЛИ <месяц год>)')
        self.textbox_date_graph.setEnabled(False)

        self.button_show_graph_by_date = QPushButton('График изменения курса по дате')
        self.button_show_graph_by_date.clicked.connect(self.show_graph_by_date)
        self.button_show_graph_by_date.setEnabled(False)

        v_layout.addWidget(self.label_info_dataset)
        v_layout.addWidget(self.button_info_of_dataset)
        v_layout.addWidget(self.button_rename_columns)
        v_layout.addWidget(self.button_check_null_fields)
        v_layout.addWidget(self.button_median_mean)
        v_layout.addWidget(self.button_describe_dataset)

        v_layout.addWidget(self.label_graphs)
        v_layout.addWidget(self.button_show_deviation_graph)
        v_layout.addWidget(self.button_show_date_graph)
        v_layout.addWidget(self.textbox_date_graph)
        v_layout.addWidget(self.button_show_graph_by_date)

        v_layout.addStretch(1) #чтобы кнопки не расплылись по форме от горизонтального слоя

        self.table = QTableWidget()
        
        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)
        h_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(h_layout)

        self.setCentralWidget(container)

    def split_fields(self, text: str) -> str:
        text = text.replace("'", "")
        res = text.split(", ")
        return res

    def choose_dataset_from_file(self):
        try:
            dat_h = DatasetHandler()
            file_dialog = QFileDialog()
            self.folder_path = file_dialog.getOpenFileName()[0]
            if(self.df is None or self.df.empty):
                self.df = dat_h.create_dataset([self.folder_path])
                self.current_fields = self.df.columns.tolist()
                self.is_loaded_dataset = True
            else:
                self.df = dat_h.create_dataset_from_files([self.folder_path], self.split_fields(self.combo_box_fields.currentText()))#self.combo_box_fields.currentText())
                self.current_fields = self.df.columns.tolist()
                self.is_loaded_dataset = True
            self.update_table()
        except Exception as e:
            self.show_message_box('Ошибка', str(e))


    def show_message_box(self, title: str, text: str):
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
        self.show_message_box('Полученные данные по дате', str(data))

    def separation_date_by_data(self):
        self.dataset_operations.separation_date_by_data(self.df)
        self.show_message_box('Успех', 'Данные отделены от даты')

    def separation_by_years(self):
        self.dataset_operations.separation_by_years(self.df)   
        self.show_message_box('Успех', 'Данные разделены по годам')

    def separation_by_weeks(self):
        self.dataset_operations.separation_by_weeks(self.df)
        self.show_message_box('Успех', 'Данные разделены по неделям')

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
            self.table.resizeColumnsToContents()

    def show_form_data(self):
        if(self.current_fields == self.split_fields("'date', 'nominal', 'value', 'vunitRate'")):
            self.currency_window = CurrencyWindow(self.df)
            self.currency_window.show()
        elif(self.current_fields == self.split_fields("'date', 'file_name', 'url', 'path'")):
            self.image_window = ImageWindow(self.df)
            self.image_window.show()

    def info_of_dataset(self):
        try:
            if(self.is_loaded_dataset == True):
                self.show_message_box('Информация о датасете', self.dataset_operations.info_of_dataset(self.df))
        except Exception as e:
            self.show_message_box('Ошибка', e)

    def rename_columns(self):
        try:
            if(self.is_loaded_dataset == True):
                self.df.columns = [self.dataset_operations.rename_columns(col) for col in self.df.columns]
                self.is_rename_columns = True
                self.update_table()
                self.button_check_null_fields.setEnabled(True)
        except Exception as e:
            self.show_message_box('Ошибка', e)


    def check_null_fields(self):
        try:
            if(self.is_rename_columns == True):
                s = self.dataset_operations.check_null_fields(self.df)
                self.dataset_operations.fill_null_fieds(self.df)
                self.update_table()
                self.show_message_box('Проверка на NaN Null', s)
                self.is_nan_check = True
                self.button_median_mean.setEnabled(True)
        except Exception as e:
            self.show_message_box('Ошибка', e)

    def median_mean(self):
        try:
            if(self.is_nan_check == True):
                self.dataset_operations.add_median_mean(self.df)
                self.is_add_median_mean = True
                self.update_table()
                self.button_describe_dataset.setEnabled(True)
                self.button_show_deviation_graph.setEnabled(True)
                self.button_show_date_graph.setEnabled(True)
                self.textbox_date_graph.setEnabled(True)
                self.button_show_graph_by_date.setEnabled(True)
        except Exception as e:
            self.show_message_box('Ошибка', e)

    def describe_dataset(self):
        try:
            if(self.is_add_median_mean == True):
                self.show_message_box('Статистическая информация', str(self.dataset_operations.describe_dataset(self.df)))
        except Exception as e:
            self.show_message_box('Ошибка', e)

    def show_deviation_graph(self):
        try:
            if(self.is_add_median_mean == True):
                self.dataset_operations.show_deviation_graph(self.df)
        except Exception as e:
            self.show_message_box('Ошибка', e)

    def show_date_graph(self):
        try:
            if(self.is_add_median_mean == True):
                self.dataset_operations.show_date_graph(self.df)
        except Exception as e:
            self.show_message_box('Ошибка', e)

    def show_graph_by_date(self):
        try:
            if(self.is_add_median_mean == True):
                res = self.textbox_date_graph.text().split()
                if len(res) == 1:
                    if len(res[0]) == 4:
                        self.dataset_operations.plot_rate_year(self.df, int(res[0]))
                    else:
                        self.dataset_operations.plot_rate_month(self.df, int(res[0]))
                else:
                    self.dataset_operations.plot_rate_year_month(self.df, int(res[1]), int(res[0]))
        except Exception:
            self.show_message_box('Ошибка', 'Дата введена неправильно! Пример ввода <месяц>, <год>, <месяц год>')

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