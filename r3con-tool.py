#!/usr/bin/env python3
"""
r3c0n-tool - Full Recon TUI
github.com/j4s3ph4/r3c0n-tool
For authorized testing only.
"""
import subprocess, datetime, pathlib, json, shutil, sys
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Button, Static, ListView, ListItem, Label, TabbedContent, TabPane, DataTable
from textual.containers import Horizontal, Vertical

HOME = pathlib.Path.home()
REPORT_DIR = HOME / "reports"
REPORT_DIR.mkdir(exist_ok=True)

ASCII = """
 █▀█ █▀▀ █▀▀ █▀█ █▄░█
 █▀▄ █▄▄ █▄▄ █▄█ █░▀█
 A minimal recon TUI
"""

def has(cmd): return shutil.which(cmd) is not None

def run(cmd, timeout=600):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return p.stdout + p.stderr
    except Exception as e:
        return f"[!] {e}"

class ReconApp(App):
    CSS = """
    Screen { background: #0f0f0f; }
    #banner { color: #ffffff; text-style: bold; dock: top; height: 6; }
    #target { width: 1fr; }
    #run { width: 16; }
    TabbedContent { height