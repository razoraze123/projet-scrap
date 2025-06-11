from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
)
from bs4 import BeautifulSoup
import sys

def generate_css_selector_from_html(html_snippet):
    soup = BeautifulSoup(html_snippet, "html.parser")
    el = soup.find()

    chain = []
    while el:
        tag = el.name
        class_name = el.get("class")
        if class_name:
            tag += "." + ".".join(class_name)
        chain.append(tag)

        # S'arrête si plusieurs enfants => ne va pas trop profondément
        children = el.find_all(recursive=False)
        if len(children) != 1:
            break
        el = children[0]

    return " ".join(chain)

class SelectorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧩 Générateur de Sélecteur CSS")
        self.setMinimumWidth(600)

        layout = QVBoxLayout()

        self.label = QLabel("Collez ici le HTML extrait :")
        self.input_box = QTextEdit()
        self.button = QPushButton("🎯 Générer le Sélecteur CSS")
        self.result_label = QLabel("Sélecteur généré :")
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        layout.addWidget(self.label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)

        self.setLayout(layout)
        self.button.clicked.connect(self.process_html)

    def process_html(self):
        html = self.input_box.toPlainText().strip()
        if html:
            try:
                selector = generate_css_selector_from_html(html)
                self.result_output.setText(selector)
            except Exception as e:
                self.result_output.setText(f"⚠️ Erreur : {str(e)}")
        else:
            self.result_output.setText("⚠️ Aucun HTML fourni.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelectorApp()
    window.show()
    sys.exit(app.exec())
