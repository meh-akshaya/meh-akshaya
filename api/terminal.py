from http.server import BaseHTTPRequestHandler
from datetime import datetime, timezone
from pathlib import Path
import requests

OWNER = "meh-akshaya"
REPO = "meh-akshaya"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url = f"https://api.github.com/repos/{OWNER}/{REPO}/commits?per_page=1"

            response = requests.get(
                url,
                headers={"User-Agent": "meh-akshaya-terminal"},
                timeout=10,
            )
            response.raise_for_status()

            commit = response.json()[0]
            date = commit["commit"]["author"]["date"]
            commit_time = datetime.fromisoformat(date.replace("Z", "+00:00"))

            now = datetime.now(timezone.utc)
            diff = now - commit_time

            days = diff.days
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60

            elapsed = (
                f"{days:02d} days "
                f"{hours:02d} hours "
                f"{minutes:02d} minutes ago"
            )

            last_login = now.strftime("%a %b %d %H:%M UTC")

            svg_path = Path(__file__).parent.parent / "assets" / "terminal.svg"
            svg = svg_path.read_text(encoding="utf-8")

            svg = svg.replace("{{LAST_LOGIN}}", last_login)
            svg = svg.replace("{{LAST_COMMIT}}", elapsed)

            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()

            self.wfile.write(svg.encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())