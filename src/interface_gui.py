"""Petite interface Tkinter pour tester le classifieur."""

import tkinter as tk
from predictor import predict_intent


def on_predict():
    text = entry.get()
    if not text.strip():
        result_var.set("")
        return
    label = predict_intent(text)
    result_var.set(label)


def main() -> None:
    global entry, result_var

    root = tk.Tk()
    root.title("\U0001F9E0 Intelligence HTML – Assistant IA")

    entry = tk.Entry(root, width=50)
    entry.pack(padx=10, pady=10)

    button = tk.Button(root, text="Pr\u00e9dire", command=on_predict)
    button.pack(pady=5)

    result_var = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_var, font=("Helvetica", 14))
    result_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
