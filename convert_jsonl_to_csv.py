import argparse
import csv
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a JSONL file with {html, selector} pairs to CSV"
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="data/dataset_with_selector.jsonl",
        help="Path to the input JSONL file",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="data/dataset_with_selector.csv",
        help="Path to the output CSV file",
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.is_file():
        alt = Path("data/dataset_with_selector_multi.jsonl")
        if in_path.name == "dataset_with_selector.jsonl" and alt.is_file():
            in_path = alt
        else:
            raise FileNotFoundError(f"Input file not found: {in_path}")

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open("r", encoding="utf-8") as f_in, out_path.open(
        "w", newline="", encoding="utf-8"
    ) as f_out:
        writer = csv.writer(f_out, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["html", "selector"])
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            html = obj.get("html")
            selector = obj.get("selector")
            if html is None or selector is None:
                continue
            writer.writerow([html, selector])


if __name__ == "__main__":
    main()
