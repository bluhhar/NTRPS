import pandas as pd
import io
import re
import matplotlib.pyplot as plt

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
        
        self.button_median_mean = QPushButton('Медианы и средний')
        self.button_median_mean.clicked.connect(self.median_mean)

        self.button_describe_dataset = QPushButton('Статистическая информация')
        self.button_describe_dataset.clicked.connect(self.describe_dataset)

        self.label_graphs = QLabel('Графики датасета')

        self.button_show_deviation_graph = QPushButton('График отклонения')
        self.button_show_deviation_graph.clicked.connect(self.show_deviation_graph)

        self.button_show_date_graph = QPushButton('График изменения курса')
        self.button_show_date_graph.clicked.connect(self.show_date_graph)

        self.textbox_date_graph = QLineEdit()
        self.textbox_date_graph.setPlaceholderText('Введите дату')

        self.button_show_graph_by_date = QPushButton('График изменения курса по дате')
        self.button_show_graph_by_date.clicked.connect(self.show_graph_by_date)

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
            else:
                self.df = dat_h.create_dataset_from_files([self.folder_path], self.split_fields(self.combo_box_fields.currentText()))#self.combo_box_fields.currentText())
                self.current_fields = self.df.columns.tolist()
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
                    #self.table.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))
            self.table.resizeColumnsToContents()

    def show_form_data(self):
        if(self.current_fields == self.split_fields("'date', 'nominal', 'value', 'vunitRate'")):
            self.currency_window = CurrencyWindow(self.df)
            self.currency_window.show()
        elif(self.current_fields == self.split_fields("'date', 'file_name', 'url', 'path'")):
            self.image_window = ImageWindow(self.df)
            self.image_window.show()

    def info_of_dataset(self):
        buf = io.StringIO()
        self.df.info(buf=buf)
        s = buf.getvalue()
        self.show_message_box('Информация о датасете', s)

    def convert_to_snake_case(self, s):
        return ''.join(['_' + i.lower() if i.isupper() else i for i in s]).lstrip('_')

    def rename_columns(self):
        self.df.columns = [self.convert_to_snake_case(col) for col in self.df.columns]
        self.update_table()

    def check_null_fields(self):
        s = self.df.isnull().sum()
        self.df.ffill(inplace=True)
        self.df.bfill(inplace=True)
        self.update_table()
        self.show_message_box('Проверка на NaN Null', str(s))

    def median_mean(self):
        median_value = self.df['vunit_rate'].median()
        mean_value = self.df['vunit_rate'].mean()

        self.df['deviation_from_median'] = self.df['vunit_rate'] - median_value
        self.df['deviation_from_mean'] = self.df['vunit_rate'] - mean_value

        self.update_table()

    def describe_dataset(self):
        s = self.df[['vunit_rate', 'deviation_from_median', 'deviation_from_mean']].describe()
        self.show_message_box('Статистическая информация', str(s))

    def show_deviation_graph(self):
        plt.figure(figsize=(12, 6))
        plt.boxplot([self.df['vunit_rate'], self.df['deviation_from_median'], self.df['deviation_from_mean']], labels=['vunit_rate', 'deviation_from_median', 'deviation_from_mean'])
        plt.title('График vunit_rate и отклонений')
        plt.show()

    def show_date_graph(self):
        self.df['date'] = pd.to_datetime(self.df['date'])

        plt.figure(figsize=(10, 6))
        plt.plot(self.df['date'], self.df['vunit_rate'])

        plt.title('Изменение курса за весь период')
        plt.xlabel('Дата')
        plt.ylabel('Курс')

        plt.show()

    def show_graph_by_date(self):
        res = self.textbox_date_graph.text().split()
        #добавить try catch
        if len(res) == 1:
            if len(res[0]) == 4:
                self.plot_rate_year(int(res[0]))
            else:
                self.plot_rate_month(int(res[0]))
        elif len(res) == 2:
            self.plot_rate_year_month(int(res[1]), int(res[0]))
        else:
            self.show_message_box('Ошибка', 'Дата введена неправильно! Пример ввода <месяц>, <год>, <месяц год>')

    def plot_rate(self, df, title):
        median_value = df['vunit_rate'].median()
        mean_value = df['vunit_rate'].mean()

        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['vunit_rate'], label='Курс')
        plt.axhline(median_value, color='r', linestyle='--', label='Медиана')
        plt.axhline(mean_value, color='g', linestyle=':', label='Среднее значение')

        plt.title(title)
        plt.xlabel('Дата')
        plt.ylabel('Курс')
        plt.legend()

        plt.show()

    def plot_rate_month(self, month):
        df_month = self.df[self.df['date'].dt.month == month]
        self.plot_rate(df_month, f'Изменение курса за {month} месяц')

    def plot_rate_year(self, year):
        df_year = self.df[self.df['date'].dt.year == year]
        self.plot_rate(df_year, f'Изменение курса за {year} год')

    def plot_rate_year_month(self, year, month):
        df_year_month = self.df[(self.df['date'].dt.year == year) & (self.df['date'].dt.month == month)]
        self.plot_rate(df_year_month, f'Изменение курса за {month} месяц в {year} год')

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