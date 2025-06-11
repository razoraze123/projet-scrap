from flask import Flask, request, render_template
from css_selector_generator import generate_selector

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    selector = ''
    html_snippet = ''
    if request.method == 'POST':
        html_snippet = request.form.get('html', '')
        selector = generate_selector(html_snippet)
    return render_template('index.html', selector=selector, html=html_snippet)

if __name__ == '__main__':
    app.run(debug=True)
