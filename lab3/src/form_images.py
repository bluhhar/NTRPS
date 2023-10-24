import pandas as pd

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap

class ImageWindow(QWidget):
    def __init__(self, df):
        super().__init__()
        
        self.setWindowTitle('Просмотр данных')

        self.label_image = QLabel()

        self.label_name = QLabel()

        self.iterator = iter(ImageIterator(df))

        self.button_next = QPushButton(">")
        self.button_next.clicked.connect(self.next_image)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label_image)
        v_layout.addWidget(self.label_name)
        v_layout.addWidget(self.button_next)

        self.setLayout(v_layout)
        self.next_image()

    def next_image(self):
        try:
            image_path = next(self.iterator)
            pixmap = QPixmap(image_path)
            self.label_image.setPixmap(pixmap.scaled(500, 500))
            self.label_name.setText(image_path)
        except StopIteration:
            pass

class ImageIterator:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.df):
            result = self.df.iloc[self.counter, 3] #ссылка сразу на картинку мб надо рефакторнуть в унивесальную функцию
            self.counter += 1
            return result
        else:
            raise StopIteration           