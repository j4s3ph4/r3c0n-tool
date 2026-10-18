#!/usr/bin/env bash
set -e
echo "[r3c0n-tool] Installing from github.com/j4s3ph4/r3c0n-tool..."

# detect Termux or Linux
if [ -n "$PREFIX" ] && [[ "$PREFIX" == *"com.termux"* ]]; then
  echo "[*] Termux detected"
  pkg update -y -q
  pkg install -y python git golang -q
else
  echo "[*] Linux/macOS detected"
  sudo apt update -qq 2>/dev/null || true
  sudo apt install -y python3-pip git golang -qq 2>/dev/null || true
fi

export PATH=$PATH:~/go/bin:$HOME/.local/bin:/data/data/com.termux/files/usr/bin

echo "[*] Installing Python deps..."
pip install textual requests --quiet 2>/dev/null || pip3 install textual requests --quiet

echo "[*] Installing Go recon tools..."
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest 2>/dev/null || true
go install github.com/projectdiscovery/httpx/cmd/httpx@latest 2>/dev/null || true
go install github.com/projectdiscovery/katana/cmd/katana@latest 2>/dev/null || true
go install github.com/lc/gau/v2/cmd/gau@latest 2>/dev/null || true

# clone or update
DIR="$HOME/r3c0n-tool"
if [ -d "$DIR" ]; then
  echo "[*] Updating existing $DIR"
  cd $DIR && git pull -q 2>/dev/null || true
else
  echo "[*] Cloning to $DIR"
  git clone https://github.com/j4s3ph4/r3c0n-tool.git $DIR -q
fi

chmod +x $DIR/*.sh $DIR/*.py 2>/dev/null || true

echo ""
echo "✅ Done!"
echo "Run: cd ~/r3c0n-tool && ./r3c0n.sh"
echo "Or:  python3 ~/r3c0n-tool/r3c0n.py"