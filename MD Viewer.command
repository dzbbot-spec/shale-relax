#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "Starting MD Viewer..."
LOG_FILE="$SCRIPT_DIR/.md_viewer.log"
rm -f "$LOG_FILE"

python3 "$SCRIPT_DIR/md_viewer_macos.py" --no-browser --file "$SCRIPT_DIR/PROGRESS.md" > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

URL=""
for _ in {1..30}; do
  if [[ -f "$LOG_FILE" ]]; then
    URL="$(python3 - "$LOG_FILE" <<'PY'
import pathlib
import re
import sys
path = pathlib.Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="ignore")
m = re.search(r"MD Viewer is running: (http://[^\s]+)", text)
print(m.group(1) if m else "")
PY
)"
    if [[ -n "$URL" ]]; then
      break
    fi
  fi
  sleep 0.2
done

if [[ -z "$URL" ]]; then
  echo "Could not detect server URL."
  echo "Check log: $LOG_FILE"
else
  echo "Open in browser: $URL"
  open "$URL" || true
fi

wait "$SERVER_PID"
