import json
from pathlib import Path

from datasets import load_dataset
from transformers import (
    AutoModelForSequenceClassification,
    DistilBertTokenizerFast,
    Trainer,
    TrainingArguments,
)
from sklearn.metrics import accuracy_score


def main():
    data_path = Path(__file__).resolve().parents[1] / "data" / "intents.jsonl"
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

    tokenized = dataset.map(tokenize, batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-multilingual-cased", num_labels=len(labels), id2label=id2label, label2id=label2id
    )

    args = TrainingArguments(
        output_dir=str(Path(__file__).resolve().parents[1] / "model" / "trained_model"),
        evaluation_strategy="epoch",
        save_strategy="epoch",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        logging_dir="logs",
    )

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = logits.argmax(-1)
        acc = accuracy_score(labels, preds)
        return {"accuracy": acc}

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)


if __name__ == "__main__":
    main()
