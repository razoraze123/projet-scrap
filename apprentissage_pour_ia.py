"""Interface graphique pour suivre l'entra\xeenement du mod\xE8le HTML selector."""

from __future__ import annotations

import argparse
import contextlib
import io
import queue
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict

import yaml
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import matplotlib

matplotlib.use("Agg")  # S\xE9curit\xE9 pour environnements sans affichage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import psutil

from src import training


# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------

def load_config(path: Path) -> Dict[str, Any]:
    """Charge et renvoie la configuration YAML."""
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Interface d'apprentissage")
    parser.add_argument("--config", required=True, help="Fichier YAML de config")
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Training thread utilities
# ---------------------------------------------------------------------------

class QueueWriter(io.TextIOBase):
    """File-like object envoyant l'output vers une queue."""

    def __init__(self, q: queue.Queue[str]):
        self.q = q

    def write(self, s: str) -> int:
        if s:
            self.q.put(s)
        return len(s)

    def flush(self):
        pass


class TrainingThread(threading.Thread):
    """Thread d'entra\xeenement du mod\xE8le."""

    def __init__(self, cfg: Dict[str, Any], log_q: queue.Queue[str], metric_q: queue.Queue[Dict[str, Any]]):
        super().__init__(daemon=True)
        self.cfg = cfg
        self.log_q = log_q
        self.metric_q = metric_q
        self.stop_event = threading.Event()

    def run(self) -> None:
        def progress(logs):
            self.metric_q.put(logs)

        stdout = QueueWriter(self.log_q)
        stderr = QueueWriter(self.log_q)
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            training.train_html_selector(progress_cb=progress, stop_event=self.stop_event)
        self.log_q.put("\nEntra\xeenement termin\xE9\n")

    def stop(self) -> None:
        self.stop_event.set()


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class TrainingApp:
    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        self.root = tk.Tk()
        self.root.title("Apprentissage HTML Selector")
        self.root.geometry("1280x720")

        self.log_q: queue.Queue[str] = queue.Queue()
        self.metric_q: queue.Queue[Dict[str, Any]] = queue.Queue()
        self.train_thread: TrainingThread | None = None
        self.start_time = None

        self._build_ui()
        self._schedule_update()

    # ------------------------ UI construction ------------------------
    def _build_ui(self) -> None:
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Aide", command=self._show_help)
        menubar.add_cascade(label="Aide", menu=help_menu)
        self.root.config(menu=menubar)

        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # Left pane: parameters
        left = ttk.Frame(main_pane, padding=10)
        main_pane.add(left, weight=1)
        ttk.Label(left, text="Param\xE8tres d'entra\xeenement", font=("TkDefaultFont", 12, "bold")).pack(anchor="w")
        params = tk.Text(left, height=10, width=40)
        params.insert(tk.END, yaml.dump(self.cfg, allow_unicode=True))
        params.configure(state="disabled")
        params.pack(fill=tk.BOTH, expand=True)

        # Right pane: plots and progress
        right = ttk.Frame(main_pane, padding=10)
        main_pane.add(right, weight=3)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4))
        self.fig = fig
        self.ax_loss = ax1
        self.ax_acc = ax2
        self.loss_values = []
        self.acc_values = []
        self.steps = []
        ax1.set_ylabel("Loss")
        ax2.set_ylabel("Accuracy")
        ax2.set_xlabel("Step")
        self.canvas = FigureCanvasTkAgg(fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.progress = ttk.Progressbar(right, length=400)
        self.progress.pack(pady=5, fill=tk.X)
        self.time_var = tk.StringVar(value="0s")
        ttk.Label(right, textvariable=self.time_var).pack(anchor="e")

        btn_frame = ttk.Frame(right)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="D\xE9marrer", command=self.start_training).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Arr\xEAter", command=self.stop_training).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exporter logs", command=self.export_logs).pack(side=tk.LEFT, padx=5)

        # Console
        self.console = ScrolledText(self.root, height=10, state="disabled")
        self.console.pack(fill=tk.BOTH, padx=5, pady=5, expand=False)

        # Status bar
        self.status_var = tk.StringVar(value="Idle")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w").pack(fill=tk.X)

    # ------------------------ UI actions ------------------------
    def start_training(self) -> None:
        if self.train_thread and self.train_thread.is_alive():
            return
        self.start_time = time.time()
        self.status_var.set("Entra\xeenement")
        self.train_thread = TrainingThread(self.cfg, self.log_q, self.metric_q)
        self.train_thread.start()

    def stop_training(self) -> None:
        if self.train_thread:
            self.train_thread.stop()
            self.status_var.set("Arr\xEAt en cours")

    def export_logs(self) -> None:
        path = Path("training_logs.txt")
        content = self.console.get("1.0", tk.END)
        path.write_text(content, encoding="utf-8")
        self.status_var.set(f"Logs export\xE9s dans {path}")

    def _show_help(self) -> None:
        messagebox.showinfo("Aide", "Lancez l'entra\xeenement puis observez les courbes.")

    # ------------------------ Update loop ------------------------
    def _schedule_update(self) -> None:
        self.root.after(500, self._update)

    def _update(self) -> None:
        self._drain_queues()
        if self.start_time and self.status_var.get().startswith("Entra"):
            elapsed = int(time.time() - self.start_time)
            self.time_var.set(f"{elapsed}s")
        self.root.after(500, self._update)

    def _drain_queues(self) -> None:
        while not self.log_q.empty():
            msg = self.log_q.get()
            self.console.configure(state="normal")
            self.console.insert(tk.END, msg)
            self.console.configure(state="disabled")
            self.console.see(tk.END)
        updated = False
        while not self.metric_q.empty():
            logs = self.metric_q.get()
            if "loss" in logs:
                self.steps.append(len(self.steps))
                self.loss_values.append(logs["loss"])
                self.ax_loss.clear()
                self.ax_loss.plot(self.steps, self.loss_values, label="train")
                self.ax_loss.legend()
                updated = True
            if "eval_accuracy" in logs:
                self.acc_values.append(logs["eval_accuracy"])
                self.ax_acc.clear()
                self.ax_acc.plot(range(len(self.acc_values)), self.acc_values, label="eval")
                self.ax_acc.legend()
                updated = True
            if "epoch" in logs and "total_flos" in logs:
                pass
        if updated:
            self.canvas.draw()
        cpu = psutil.cpu_percent(interval=None)
        self.status_var.set(f"{self.status_var.get().split(' ')[0]} | CPU {cpu}%")

    # ------------------------ Public API ------------------------
    def run(self) -> None:
        self.root.mainloop()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv=None) -> None:
    args = parse_args(argv)
    cfg = load_config(Path(args.config))
    app = TrainingApp(cfg)
    app.run()


if __name__ == "__main__":
    main()
