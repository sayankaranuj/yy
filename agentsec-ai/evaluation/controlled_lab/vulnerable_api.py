"""Local-only deterministic fixture for scanner evaluation.

Run with ``python -m evaluation.controlled_lab.vulnerable_api`` and point
authorized scans at ``http://127.0.0.1:8765`` in development mode.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class VulnerableFixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        query = parse_qs(urlparse(self.path).query)
        if self.path.startswith("/xss"):
            body = f"<html><body>{query.get('q', [''])[0]}</body></html>"
            self._send(200, body, "text/html")
            return
        if self.path.startswith("/secret"):
            self._send(200, '{"api_key":"fixture-secret-redacted"}', "application/json")
            return
        self._send(200, "controlled fixture: no finding expected", "text/plain")

    def log_message(self, *_args: object) -> None:
        return

    def _send(self, code: int, body: str, content_type: str) -> None:
        encoded = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    HTTPServer((host, port), VulnerableFixtureHandler).serve_forever()


if __name__ == "__main__":
    serve()
