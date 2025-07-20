from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTextEdit, QLabel, QMainWindow, QHBoxLayout
)
from Hash import HashTable


class SearchWindow(QWidget):
    def __init__(self, table):
        super().__init__()
        self.setWindowTitle("Buscar palabra")
        self.table = table
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Palabra a buscar")
        layout.addWidget(self.word_input)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        search_btn = QPushButton("Buscar")
        search_btn.clicked.connect(self.search_word)
        layout.addWidget(search_btn)

        self.setLayout(layout)

    def search_word(self):
        word = self.word_input.text()
        definition = self.table.search(word)
        if definition:
            self.result.setText(f"{word}: {definition}")
        else:
            self.result.setText("Palabra no encontrada.")


class AddWindow(QWidget):
    def __init__(self, table):
        super().__init__()
        self.setWindowTitle("Agregar o eliminar palabra")
        self.table = table
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Palabra")
        layout.addWidget(self.word_input)

        self.definition_input = QLineEdit()
        self.definition_input.setPlaceholderText("Definición")
        layout.addWidget(self.definition_input)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        add_btn = QPushButton("Agregar / Actualizar")
        add_btn.clicked.connect(self.add_word)
        layout.addWidget(add_btn)

        delete_btn = QPushButton("Eliminar palabra")
        delete_btn.clicked.connect(self.delete_word)
        layout.addWidget(delete_btn)

        self.setLayout(layout)

    def add_word(self):
        word = self.word_input.text()
        definition = self.definition_input.text()
        self.table.insert(word, definition)
        self.result.setText(f"{word} agregado o actualizado.")

    def delete_word(self):
        word = self.word_input.text()
        if self.table.delete(word):
            self.result.setText(f"{word} eliminado.")
        else:
            self.result.setText("Palabra no encontrada.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diccionario Inteligente - Menú Principal")
        self.resize(300, 150)

        self.table = HashTable()

        central_widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Selecciona una opción:")
        layout.addWidget(label)

        search_btn = QPushButton("Buscar palabra")
        search_btn.clicked.connect(self.open_search)
        layout.addWidget(search_btn)

        add_btn = QPushButton("Agregar o eliminar palabra")
        add_btn.clicked.connect(self.open_add)
        layout.addWidget(add_btn)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_search(self):
        self.search_window = SearchWindow(self.table)
        self.search_window.show()

    def open_add(self):
        self.add_window = AddWindow(self.table)
        self.add_window.show()
