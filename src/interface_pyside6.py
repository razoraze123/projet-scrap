"""PySide6 GUI to predict CSS selector from question and HTML."""

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton
)
from PySide6.QtCore import Qt
import sys

from src.html_selector import predire_selecteur
from src.memoire_generale import ajouter_interaction


class SelectorWindow(QWidget):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("\U0001F9E0 Sélecteur CSS")
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Question:"))
        self.question_edit = QLineEdit()
        layout.addWidget(self.question_edit)

        layout.addWidget(QLabel("Bloc HTML:"))
        self.html_edit = QTextEdit()
        layout.addWidget(self.html_edit)

        self.button = QPushButton("Prédire")
        self.button.clicked.connect(self.on_predict)
        layout.addWidget(self.button)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

    def on_predict(self) -> None:
        question = self.question_edit.text()
        html = self.html_edit.toPlainText()
        if not question.strip() or not html.strip():
            self.result_label.setText("")
            return
        ajouter_interaction("texte_libre", {"message": question})
        try:
            selector = predire_selecteur(question, html)
            ajouter_interaction(
                "prediction",
                {"question": question, "html": html, "reponse": selector},
            )
            ajouter_interaction("reponse", {"texte": selector})
        except Exception as e:  # pragma: no cover
            ajouter_interaction("erreur", {"exception": str(e)})
            selector = ""
        self.result_label.setText(f"\U0001F9E0 Sélecteur prédit : {selector}")


def main() -> None:
    """Entry point for the PySide6 interface."""
    app = QApplication(sys.argv)
    window = SelectorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
