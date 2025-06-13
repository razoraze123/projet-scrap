"""Utility training functions for CLI and GUI."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, Optional, Any
import config

from datasets import load_dataset
from transformers import (
    AutoModelForSequenceClassification,
    DistilBertTokenizerFast,
    Trainer,
    TrainingArguments,
    TrainerCallback,
)
from sklearn.metrics import accuracy_score


class ProgressCallback(TrainerCallback):
    """Report training progress through a callback."""

    def __init__(self, callback: Callable[[Dict[str, Any]], None], stop_event=None):
        self.callback = callback
        self.stop_event = stop_event

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs and self.callback:
            self.callback(logs)
        if self.stop_event and self.stop_event.is_set():
            control.should_training_stop = True


def train_classifier(progress_cb: Optional[Callable[[Dict[str, Any]], None]] = None,
                     stop_event=None) -> None:
    """Train the intent classifier."""
    data_path = config.INTENTS_FILE
    if not data_path.is_file():
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    dataset = load_dataset("json", data_files=str(data_path))
    dataset = dataset["train"].train_test_split(test_size=0.2, seed=42)

    labels = sorted(set(dataset["train"]["label"]))
    label2id = {l: i for i, l in enumerate(labels)}
    id2label = {i: l for l, i in label2id.items()}

    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-multilingual-cased")

    def tokenize(batch):
        enc = tokenizer(batch["text"], truncation=True, padding="max_length", max_length=32)
        enc["labels"] = [label2id[l] for l in batch["label"]]
        return enc

    tokenized = dataset.map(tokenize, batched=True, remove_columns=["text", "label"])

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-multilingual-cased", num_labels=len(labels), id2label=id2label, label2id=label2id
    )

    args = TrainingArguments(
        output_dir=str(config.CLASSIFIER_MODEL_DIR),
        num_train_epochs=config.TRAIN_EPOCHS,
        per_device_train_batch_size=config.TRAIN_BATCH_SIZE,
        learning_rate=config.LEARNING_RATE,
        logging_dir="logs",
        logging_steps=10,
        save_steps=50,
        save_total_limit=1,
        do_train=True,
    )

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = logits.argmax(-1)
        acc = accuracy_score(labels, preds)
        return {"accuracy": acc}

    callbacks = []
    if progress_cb:
        callbacks.append(ProgressCallback(progress_cb, stop_event))

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
        callbacks=callbacks,
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)


def train_html_selector(progress_cb: Optional[Callable[[Dict[str, Any]], None]] = None,
                        stop_event=None) -> None:
    """Train the HTML selector model."""
    data_path = config.HTML_SELECTOR_FILE
    if not data_path.is_file():
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    dataset = load_dataset("json", data_files=str(data_path))
    dataset = dataset["train"].train_test_split(test_size=0.1, seed=42)

    labels = sorted(set(dataset["train"]["label"]) | set(dataset["test"]["label"]))
    label2id = {l: i for i, l in enumerate(labels)}
    id2label = {i: l for l, i in label2id.items()}

    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-multilingual-cased")

    def tokenize(batch):
        texts = [f"[QUESTION] {q} [HTML] {h}" for q, h in zip(batch["question"], batch["html"])]
        enc = tokenizer(texts, truncation=True, padding="max_length", max_length=128)
        enc["labels"] = [label2id[l] for l in batch["label"]]
        return enc

    tokenized = dataset.map(tokenize, batched=True, remove_columns=["question", "html", "label"])

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-multilingual-cased",
        num_labels=len(labels),
        id2label=id2label,
        label2id=label2id,
    )

    args = TrainingArguments(
        output_dir=str(config.HTML_SELECTOR_MODEL_DIR),
        num_train_epochs=3,
        per_device_train_batch_size=config.TRAIN_BATCH_SIZE,
        learning_rate=config.LEARNING_RATE,
        logging_dir="logs",
        logging_steps=10,
        save_steps=100,
        save_total_limit=1,
        do_train=True,
        do_eval=True,
    )

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = logits.argmax(-1)
        acc = accuracy_score(labels, preds)
        return {"accuracy": acc}

    callbacks = []
    if progress_cb:
        callbacks.append(ProgressCallback(progress_cb, stop_event))

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
        callbacks=callbacks,
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
