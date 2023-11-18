import matplotlib.pyplot as plt

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit

class PlotChooseDateForm(QWidget):
    def __init__(self, df):
        super().__init__()
        self.initUI()

        self.df = df

    def initUI(self):
        self.setWindowTitle('My Form')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text_field = QLineEdit()
        self.layout.addWidget(self.text_field)

        self.ok_button = QPushButton('OK')
        self.layout.addWidget(self.ok_button)
        self.ok_button.clicked.connect(self.plot_rate_month)

    def plot_rate_month(self, month):
        #month = self.text_field.text()
        df_month = self.df[self.df['date'].dt.month == month]

        median_value = df_month['vunit_rate'].median()
        mean_value = df_month['vunit_rate'].mean()

        plt.figure(figsize=(10, 6))
        plt.plot(df_month['date'], df_month['vunit_rate'], label='Курс')
        plt.axhline(median_value, color='r', linestyle='--', label='Медиана')
        plt.axhline(mean_value, color='g', linestyle=':', label='Среднее значение')

        plt.title('Изменение курса за месяц')
        plt.xlabel('Дата')
        plt.ylabel('Курс')
        plt.legend()

        plt.show()
