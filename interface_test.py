from detecteur import generer_selecteur

if __name__ == "__main__":
    print("\U0001F3A7 Interface Test – Analyse de sélecteurs CSS avec IA\n")
    try:
        while True:
            q = input("❓ Question → ")
            path = input("\U0001F4C4 Fichier HTML → ")
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            sel = generer_selecteur(html, q)
            print(f"\n\U0001F3AF Sélecteur généré : {sel}\n")
    except KeyboardInterrupt:
        print("\n\U0001F44B Interface terminée.")
