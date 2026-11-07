"""Smoke take-home solution: /health, /echo, /sum and the E1 /upper.
Stdlib only; listens on 0.0.0.0:8080."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(fmt % args, flush=True)

    def reply(self, status, body):
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def error(self, status, code, message):
        self.reply(status, {"error": {"code": code, "message": message}})

    def do_GET(self):
        url = urlparse(self.path)
        query = {k: v[0] for k, v in parse_qs(url.query).items()}
        if url.path == "/health":
            return self.reply(200, {"status": "ok"})
        if url.path == "/sum":
            try:
                return self.reply(200, {"sum": int(query["a"]) + int(query["b"])})
            except (KeyError, ValueError):
                return self.error(422, "VALIDATION", "a and b must both be integers")
        if url.path == "/upper":
            return self.reply(200, {"text": query.get("text", "").upper()})
        self.error(404, "NOT_FOUND", "no such path")

    def do_POST(self):
        if urlparse(self.path).path != "/echo":
            return self.error(404, "NOT_FOUND", "no such path")
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("content-length") or 0)) or b"{}")
        except ValueError:
            return self.error(422, "VALIDATION", "body must be JSON")
        text = body.get("text") if isinstance(body, dict) else None
        if not isinstance(text, str):
            return self.error(422, "VALIDATION", "text must be a string")
        self.reply(200, {"text": text, "length": len(text)})


def server(port=None):
    return ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8080)) if port is None else port), Handler)


if __name__ == "__main__":
    print("listening on 8080", flush=True)
    server().serve_forever()
