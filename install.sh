#!/usr/bin/env bash
echo "[r3c0n] Installing..."
export PATH=$PATH:~/go/bin
pkg update -y -q 2>/dev/null || true
pkg install -y python git golang -q 2>/dev/null || true
pip install textual requests -q
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest 2>/dev/null || true
go install github.com/projectdiscovery/httpx/cmd/httpx@latest 2>/dev/null || true
chmod +x ~/r3c0n/*.sh ~/r3c0n/*.py 2>/dev/null || true
echo "[r3c0n] Done! cd ~/r3c0n && ./r3c0n.sh"