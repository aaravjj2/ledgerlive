"""mock_airia_receiver.py — Local mock Airia webhook receiver.

Runs on localhost, receives webhook POSTs from the LedgerLive agent,
and logs them to artifacts/airia/webhook_log.jsonl.

Usage:
    python tools/airia_loop/mock_airia_receiver.py [--port 9099]
"""
from __future__ import annotations

import argparse
import json
import datetime as dt
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG_PATH = Path(__file__).resolve().parent.parent.parent / "artifacts" / "airia" / "webhook_log.jsonl"


class AiriaReceiverHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""

        try:
            payload = json.loads(body)
        except Exception:
            payload = {"raw": body.decode("utf-8", errors="replace")}

        entry = {
            "received_at": dt.datetime.utcnow().isoformat(),
            "path": self.path,
            "headers": dict(self.headers),
            "payload": payload,
        }

        # Log to file
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")

        print(f"[receiver] POST {self.path} — logged ({len(body)} bytes)")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "received"}).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        entries = []
        if LOG_PATH.exists():
            lines = LOG_PATH.read_text(encoding="utf-8").strip().split("\n")
            for line in lines[-50:]:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass

        self.wfile.write(json.dumps({"entries": entries, "total": len(entries)}).encode())

    def log_message(self, format, *args):
        pass  # suppress default logging


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9099)
    args = parser.parse_args()

    server = HTTPServer(("127.0.0.1", args.port), AiriaReceiverHandler)
    print(f"[Airia Mock Receiver] Listening on http://127.0.0.1:{args.port}")
    print(f"[Airia Mock Receiver] Logs → {LOG_PATH}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Airia Mock Receiver] Stopped.")


if __name__ == "__main__":
    main()
