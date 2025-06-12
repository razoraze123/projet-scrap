"""Interface Tkinter pour tester la prédiction de sélecteur CSS."""

import tkinter as tk
from html_selector import predire_selecteur
from src.memoire_generale import ajouter_interaction


def on_predict():
    question = question_entry.get()
    html = html_text.get("1.0", tk.END)
    if not question.strip() or not html.strip():
        result_var.set("")
        return
    ajouter_interaction("texte_libre", {"message": question})
    try:
        selector = predire_selecteur(question, html)
        ajouter_interaction(
            "prediction",
            {"question": question, "html": html, "reponse": selector},
        )
        ajouter_interaction("reponse", {"texte": selector})
    except Exception as e:  # pragma: no cover - UI exceptions aren't tested
        ajouter_interaction("erreur", {"exception": str(e)})
        selector = ""
    result_var.set(f"\U0001F9E0 Sélecteur prédit : {selector}")


def main() -> None:
    global question_entry, html_text, result_var

    root = tk.Tk()
    root.title("\U0001F9E0 Prédicteur de sélecteur CSS")

    tk.Label(root, text="Question:").pack(anchor="w", padx=10)
    question_entry = tk.Entry(root, width=60)
    question_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(root, text="Bloc HTML:").pack(anchor="w", padx=10)
    html_text = tk.Text(root, width=60, height=10)
    html_text.pack(fill="both", padx=10, pady=5)

    button = tk.Button(root, text="Prédire", command=on_predict)
    button.pack(pady=5)

    result_var = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_var, font=("Helvetica", 12))
    result_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
