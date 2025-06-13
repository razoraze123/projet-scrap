from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from apprentissage_pour_ia import load_config, parse_args


def test_load_config(tmp_path):
    cfg_file = tmp_path / "c.yaml"
    cfg_file.write_text("epochs: 2\n")
    cfg = load_config(cfg_file)
    assert cfg["epochs"] == 2


def test_parse_args():
    args = parse_args(["--config", "file.yaml"])
    assert args.config == "file.yaml"
