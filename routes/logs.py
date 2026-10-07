from flask import Blueprint
import subprocess
from pathlib import Path
from ui.styles import CSS

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/logs/wildtrace")
def view_wildtrace_logs():
    try:
        folder = Path("/home/eloise/Desktop/WildTrace/logs/")
        if not folder.exists() or not folder.is_dir():
            return "Logs folder not found."

        files = [f for f in folder.glob("*.log") if f.is_file()]
        if not files:
            return "No log files found."

        last_file = max(files, key=lambda f: f.stat().st_mtime)
        content = last_file.read_text()

        return f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            {CSS}
        </head>
        <body>
            <div class="panel-wide">
                <h2 id="title">WildTrace</h2>
                <div class="subtitle" id="subtitle">Application logs</div>
                <pre>{content}</pre>
                <form action="/"><button class="btn secondary">Back</button></form>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"Error reading logs: {e}"


@logs_bp.route("/logs/flask")
def view_flask_logs():
    try:
        result = subprocess.check_output(
            ["journalctl", "-u", "wildtrace-admin", "-b", "--no-pager"],
            text=True
        )

        return f"""
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            {CSS}
        </head>
        <body>
            <div class="panel-wide">
                <h2 id="title">System</h2>
                <div class="subtitle" id="subtitle">Service logs</div>
                <pre>{result}</pre>
                <form action="/"><button class="btn secondary">Back</button></form>
            </div>
        </body>
        </html>
        """
    except subprocess.CalledProcessError as e:
        return f"Error reading systemd logs: {e}"
