#!/usr/bin/env python3
import subprocess, datetime, pathlib
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, ListView, ListItem, Label
from textual.containers import Horizontal

REPORT_DIR = pathlib.Path.home() / "reports"
REPORT_DIR.mkdir(exist_ok=True)

def run_cmd(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300).stdout
    except Exception as e:
        return str(e)

class ReconApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Input(placeholder="target.com", id="target")
            yield Button("Run Recon", variant="primary", id="run")
        yield Static("Logs: waiting...", id="log")
        yield ListView(id="results")
        yield Footer()
    
    def on_button_pressed(self, event):
        if event.button.id == "run":
            target = self.query_one("#target", Input).value.strip()
            if not target: return
            log = self.query_one("#log", Static)
            results = self.query_one("#results", ListView)
            log.update(f"Running on {target}...")
            out_dir = REPORT_DIR / f"{target}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            out_dir.mkdir(parents=True, exist_ok=True)
            sub_file = out_dir / "subs.txt"
            run_cmd(f"subfinder -d {target} -silent -o {sub_file} 2>&1 || echo no-subfinder")
            live_file = out_dir / "live.txt"
            if sub_file.exists():
                run_cmd(f"cat {sub_file} | httpx -silent -o {live_file} 2>&1 || cat {sub_file} > {live_file}")
            results.clear()
            if live_file.exists():
                with open(live_file) as f:
                    for l in f.readlines()[:100]:
                        results.append(ListItem(Label(l.strip())))
            log.update(f"DONE {out_dir}")

def main():
    ReconApp().run()

if __name__ == "__main__":
    main()