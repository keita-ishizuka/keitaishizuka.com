"""Static file server for researcher page."""
import http.server
import os

PORT = 8400
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Clean URL support: /path → /path/index.html
        path = self.path.split("?")[0].split("#")[0]
        full = os.path.join(DIRECTORY, path.lstrip("/"))
        if not os.path.exists(full) and not path.endswith("/"):
            index = os.path.join(full, "index.html")
            if os.path.exists(index):
                self.path = path.rstrip("/") + "/index.html"
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "public, max-age=3600")
        super().end_headers()

    def log_message(self, format, *args):
        pass


httpd = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
print(f"Serving {DIRECTORY} on port {PORT}", flush=True)
httpd.serve_forever()
