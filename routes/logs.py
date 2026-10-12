from flask import Blueprint
from markupsafe import escape
from services.logging_config import FLASK_LOG_FILE
import subprocess
from shutil import which
from pathlib import Path
from ui.styles import CSS
from services.wildtrace import WILDTRACE_ROOT

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/logs/wildtrace")
def view_wildtrace_logs():
    try:
        folder = WILDTRACE_ROOT / "logs"
        if not folder.exists() or not folder.is_dir():
            return "Logs folder not found."

        files = [f for f in folder.glob("*.log") if f.is_file()]
        if not files:
            return "No log files found."

        last_file = max(files, key=lambda f: f.stat().st_mtime)
        content = escape(last_file.read_text(encoding="utf-8", errors="replace"))

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
        if which("journalctl") is None:
            if FLASK_LOG_FILE.is_file():
                with FLASK_LOG_FILE.open("rb") as file:
                    file.seek(0, 2)
                    size = file.tell()
                    file.seek(max(0, size - 100_000))
                    if size > 100_000:
                        file.readline()
                    result = file.read().decode("utf-8", errors="replace")
            else:
                result = "Aucun log Flask enregistré pour le moment."
        else:
            result = subprocess.check_output(
                ["journalctl", "-u", "wildtrace-admin", "-b", "--no-pager"],
                text=True
            )
        result = escape(result)

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
    except (subprocess.CalledProcessError, OSError) as e:
        return f"Error reading systemd logs: {e}"
