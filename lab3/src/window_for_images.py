import pandas as pd

from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PyQt6.QtGui import QPixmap

class ImageWindow(QWidget):
    def __init__(self, df):
        super().__init__()

        self.label_image = QLabel()

        self.label_name = QLabel()

        self.df = df
        self.current_image_index = 0

        self.button_previous = QPushButton("<")
        self.button_previous.clicked.connect(self.show_previous_image)
        self.button_next = QPushButton(">")
        self.button_next.clicked.connect(self.show_next_image)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label_image)
        v_layout.addWidget(self.label_name)
        v_layout.addWidget(self.button_previous)
        v_layout.addWidget(self.button_next)

        self.setLayout(v_layout)
        self.show_image()

    def show_image(self):
        image_path = self.df.loc[self.current_image_index, 'path']
        pixmap = QPixmap(image_path)
        self.label_image.setPixmap(pixmap.scaled(500, 500))
        self.label_name.setText(image_path)

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()

    def show_next_image(self):
        if self.current_image_index < len(self.df) - 1:
            self.current_image_index += 1
            self.show_image()

def main():
    app = QApplication([])

    df = pd.read_csv('C:\\Users\\bluh\\Desktop\\Python\\lab3\\outputs\\datasets\\images\\Arthas Wrath of the Lich King_dataset.csv')

    window = ImageWindow(df)
    window.show()

    app.exec()
    
if __name__ == '__main__':
    main()