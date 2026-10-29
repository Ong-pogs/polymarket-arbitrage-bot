"""Local Predictefy scanner and historical price-study dashboard."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent


def api_key():
    value = os.environ.get("PREDICTEFY_API_KEY", "").strip()
    if value:
        return value
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            key, sep, value = line.strip().partition("=")
            if sep and key.strip() == "PREDICTEFY_API_KEY":
                return value.strip().strip("\"").strip("'")
    return ""


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "public"), **kwargs)

    def json_response(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/terminal":
            body = subprocess.check_output(
                [sys.executable, str(ROOT / "tools/analyze.py")], cwd=ROOT
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/scan":
            key = api_key()
            if not key:
                self.json_response(400, {"success": False, "error": "Set PREDICTEFY_API_KEY in .env or the environment."})
                return
            request = urllib.request.Request(
                "https://data.predictefy.com/api/router/fetchArbitrage?contracts=100&executableOnly=true&limit=50",
                headers={"Authorization": "Bearer " + key},
            )
            try:
                with urllib.request.urlopen(request, timeout=45) as response:
                    payload = json.loads(response.read())
                (ROOT / "public/latest-scan.json").write_text(json.dumps(payload), encoding="utf-8")
                self.json_response(200, payload)
            except urllib.error.HTTPError as error:
                self.json_response(502, {"success": False, "error": "Predictefy request failed", "upstreamStatus": error.code})
            except (urllib.error.URLError, TimeoutError, ValueError):
                self.json_response(502, {"success": False, "error": "Could not fetch a valid Predictefy response."})
            return
        super().do_GET()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8862"))
    print(f"Polymarket arbitrage scanner | http://127.0.0.1:{port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
