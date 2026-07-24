from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml")
        self.end_headers()

        self.wfile.write(b"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="60">
<text x="20" y="35" font-size="20">Terminal Works!</text>
</svg>""")