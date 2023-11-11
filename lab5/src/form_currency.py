import pandas as pd

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

class CurrencyWindow(QWidget):
    def __init__(self, df):
        super().__init__()
        
        self.setWindowTitle('Просмотр данных')

        self.label_name = QLabel()

        self.iterator = iter(DataIterator(df))

        self.button_next = QPushButton(">")
        self.button_next.clicked.connect(self.next_currency)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label_name)
        v_layout.addWidget(self.button_next)

        self.setLayout(v_layout)
        self.next_currency()

    def next_currency(self):
        try:
            data = next(self.iterator)
            self.label_name.setText(str(data))
        except StopIteration:
            pass

class DataIterator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.df):
            result = tuple(self.df.iloc[self.counter])
            self.counter += 1
            return result
        else:
            raise StopIteration         