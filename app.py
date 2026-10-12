from pathlib import Path
from flask import Flask, request
from services.logging_config import configure_logging
from routes.ui import ui_bp
from routes.network import network_bp
from routes.actions import actions_bp
from routes.logs import logs_bp

app = Flask(__name__)
configure_logging(app)


@app.after_request
def log_response(response):
    app.logger.info("%s %s -> %s", request.method, request.path, response.status_code)
    return response


app.register_blueprint(ui_bp)
app.register_blueprint(network_bp)
app.register_blueprint(actions_bp)
app.register_blueprint(logs_bp)

if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent
    port = 5500 if (project_dir / ".venv").is_dir() else 5000
    app.run(host="0.0.0.0", port=port, debug=True)
