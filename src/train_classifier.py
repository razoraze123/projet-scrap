"""CLI entry point for training the intent classifier."""

from src import training


def main() -> None:
    """Run the classifier training using :mod:`src.training`."""
    training.train_classifier()


if __name__ == "__main__":
    main()
