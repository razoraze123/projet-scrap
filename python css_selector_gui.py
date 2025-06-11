from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
)
from html_content_finder import ContentFinder
from selector_utils import generate_css_selector_from_html
import sys

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
                finder = ContentFinder(html)
                element = finder.find_content_element()
                if element:
                    parts = []
                    robust = finder.get_robust_selector()
                    if robust:
                        parts.append(robust)
                    short = finder.get_short_selector()
                    if short and short != robust:
                        parts.append(short)
                    xpath = finder.get_xpath()
                    if xpath:
                        parts.append(xpath)
                    if parts:
                        self.result_output.setText("\n".join(parts))
                    else:
                        self.result_output.setText("Aucun sélecteur généré.")
                else:
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
