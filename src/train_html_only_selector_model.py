"""CLI entry point for training HTML-only selector model."""

from src import training


def main() -> None:
    """Run the HTML-only selector training."""
    training.train_html_only_selector()


if __name__ == "__main__":
    main()
