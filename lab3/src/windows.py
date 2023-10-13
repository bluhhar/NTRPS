from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit
from PyQt6.QtCore import QDate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.file_path = ""

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

    def pick_file(self):
        file_dialog = QFileDialog()
        self.file_path = file_dialog.getOpenFileName()[0]

    def search_date(self):
        date_str = self.date_input.text()
        date = QDate.fromString(date_str, "dd.MM.yyyy")


app = QApplication([])
window = MainWindow()
window.show()

app.exec()