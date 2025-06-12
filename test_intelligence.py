from intelligence import analyser_question


def test_titre():
    question = "Quel est le titre de l'article ?"
    assert analyser_question(question, debug=False) in ["titre"]


def test_image():
    question = "Montre-moi la photo du produit"
    assert analyser_question(question, debug=False) in ["image"]
