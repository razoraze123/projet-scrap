import click
import importlib

@click.group()
def cli():
    """Utility command line interface."""
    pass

@cli.command()
def generate():
    """Generate the example HTML dataset."""
    mod = importlib.import_module('generate_dataset')
    mod.main()

@cli.command('train-classifier')
def train_classifier():
    """Train the intent classifier."""
    from src import train_classifier as tc
    tc.main()

@cli.command('train-selector')
def train_selector():
    """Train the HTML selector model."""
    from src import train_html_selector_model as th
    th.main()


@cli.command('train-selector-html')
def train_selector_html():
    """Train the HTML-only selector model."""
    from src import train_html_only_selector_model as thh
    thh.main()


@cli.command('predict-selector-html')
@click.argument('file', required=False, type=click.Path())
def predict_selector_html(file):
    """Predict CSS selector from a HTML snippet."""
    from src import html_only_predictor as hp
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
    else:
        import sys
        html = sys.stdin.read()
    selector = hp.predict_selector(html)
    click.echo(selector)

@cli.command()
def serve():
    """Run the Flask web interface."""
    import web_interface as wi
    import config
    wi.app.run(debug=config.FLASK_DEBUG, host=config.FLASK_HOST, port=config.FLASK_PORT)

if __name__ == '__main__':
    cli()
