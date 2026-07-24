from datetime import datetime, timezone
import subprocess
from pathlib import Path


def handler(request):
    try:
        timestamp = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct"]
        ).decode().strip()

        commit_time = datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
        now = datetime.now(timezone.utc)

        diff = now - commit_time

        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60

        elapsed = (
            f"{days:02d} days {hours:02d} hours "
            f"{minutes:02d} minutes ago"
        )

        last_login = now.strftime("%a %b %d %H:%M UTC")

        svg_path = Path(__file__).parent.parent / "assets" / "terminal.svg"

        svg = svg_path.read_text()

        svg = svg.replace("{{LAST_LOGIN}}", last_login)
        svg = svg.replace("{{LAST_COMMIT}}", elapsed)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/svg+xml",
                "Cache-Control": "no-cache",
            },
            "body": svg,
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e),
        }