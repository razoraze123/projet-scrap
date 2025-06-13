from flask import Flask, request, render_template
from css_selector_generator import generate_selector
from src.memoire_generale import ajouter_interaction
import config

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    selector = ''
    html_snippet = ''
    if request.method == 'POST':
        html_snippet = request.form.get('html', '')
        ajouter_interaction("texte_libre", {"message": html_snippet})
        try:
            selector = generate_selector(html_snippet)
            ajouter_interaction("prediction", {"html": html_snippet, "reponse": selector})
            ajouter_interaction("reponse", {"texte": selector})
        except Exception as e:
            ajouter_interaction("erreur", {"exception": str(e)})
            selector = ''
    return render_template('index.html', selector=selector, html=html_snippet)

if __name__ == '__main__':
    app.run(debug=config.FLASK_DEBUG, host=config.FLASK_HOST, port=config.FLASK_PORT)
