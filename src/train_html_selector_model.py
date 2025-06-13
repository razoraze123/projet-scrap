"""CLI entry point for training the HTML selector model."""

from src import training


def main() -> None:
    """Run the selector model training using :mod:`src.training`."""
    training.train_html_selector()


if __name__ == "__main__":
    main()
