from detecteur import generer_selecteur
from src.memoire_generale import ajouter_interaction

if __name__ == "__main__":
    print("\U0001F3A7 Interface Test – Analyse de sélecteurs CSS avec IA\n")
    try:
        while True:
            q = input("❓ Question → ")
            path = input("\U0001F4C4 Fichier HTML → ")
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            ajouter_interaction("texte_libre", {"message": q})
            try:
                sel = generer_selecteur(html, q)
                ajouter_interaction("reponse", {"texte": sel})
            except Exception as e:
                ajouter_interaction("erreur", {"exception": str(e)})
                raise
            print(f"\n\U0001F3AF Sélecteur généré : {sel}\n")
    except KeyboardInterrupt:
        print("\n\U0001F44B Interface terminée.")
