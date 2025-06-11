from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
)
from bs4 import BeautifulSoup
import sys

# Mots-clés et listes d'exclusions pour le repérage de l'élément pertinent
CONTENT_KEYWORDS = ["rte", "content", "desc", "description", "prose"]
INLINE_TAGS = ["span", "b", "i", "strong", "em", "a"]
GENERIC_CLASSES = ["tabcontent", "container", "wrapper"]

def generate_css_selector_from_html(html_snippet):
    """Retourne un sélecteur CSS pour l'extrait fourni.

    La fonction recherche d'abord un noeud dont les classes contiennent un des
    :data:`CONTENT_KEYWORDS` tout en évitant celles listées dans
    :data:`GENERIC_CLASSES`. Si rien n'est trouvé, elle se rabat sur la première
    balise de l'extrait (ancienne heuristique).

    Une fois la balise cible identifiée, on remonte dans l'arbre jusqu'à la
    racine ou jusqu'à rencontrer un ancêtre possédant une classe générique. Les
    balises mentionnées dans :data:`INLINE_TAGS` sont ignorées afin de ne pas
    rendre le sélecteur inutilement verbeux.
    """

    soup = BeautifulSoup(html_snippet, "html.parser")

    candidate = None
    for el in soup.find_all(True):
        classes = el.get("class", [])
        class_str = " ".join(classes)
        if (classes and
                any(kw in class_str for kw in CONTENT_KEYWORDS) and
                not any(gc in classes for gc in GENERIC_CLASSES)):
            candidate = el
            break

    if not candidate:
        candidate = soup.find()

    chain = []
    el = candidate
    while el and el != soup:
        if el.name not in INLINE_TAGS:
            tag = el.name
            classes = el.get("class")
            if classes:
                tag += "." + ".".join(classes)
            chain.append(tag)

        parent = el.parent if el.parent != el else None
        if not parent or any(gc in parent.get("class", []) for gc in GENERIC_CLASSES):
            break
        el = parent

    selector = " ".join(reversed(chain))

    # Seconde variante optionnelle : inclure le parent direct si pertinent
    alt_selector = None
    parent = candidate.parent if candidate else None
    if parent and parent != soup and parent.name not in INLINE_TAGS and not any(
        gc in parent.get("class", []) for gc in GENERIC_CLASSES
    ):
        tag = parent.name
        classes = parent.get("class")
        if classes:
            tag += "." + ".".join(classes)
        chain_alt = chain + [tag]
        alt_selector = " ".join(reversed(chain_alt))

    if alt_selector and alt_selector != selector:
        return selector + "\n" + alt_selector
    return selector

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
