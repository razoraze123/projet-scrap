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

@cli.command()
def serve():
    """Run the Flask web interface."""
    import web_interface as wi
    import config
    wi.app.run(debug=config.FLASK_DEBUG, host=config.FLASK_HOST, port=config.FLASK_PORT)

if __name__ == '__main__':
    cli()
