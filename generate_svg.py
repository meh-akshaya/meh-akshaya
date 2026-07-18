from datetime import datetime, timezone
import subprocess

# Get latest commit timestamp
timestamp = subprocess.check_output(
    ["git", "log", "-1", "--format=%ct"]
).decode().strip()

commit_time = datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
now = datetime.now(timezone.utc)

diff = now - commit_time

days = diff.days
hours = diff.seconds // 3600
minutes = (diff.seconds % 3600) // 60

elapsed = f"{days:02d} days {hours:02d} hours {minutes:02d} minutes ago"

last_login = now.astimezone().strftime("%a %b %d %H:%M")

with open("assets/terminal.svg", "r") as f:
    svg = f.read()

svg = svg.replace("{{LAST_LOGIN}}", last_login)
svg = svg.replace("{{LAST_COMMIT}}", elapsed)

with open("assets/commit-counter.svg", "w") as f:
    f.write(svg)

print("SVG updated.")