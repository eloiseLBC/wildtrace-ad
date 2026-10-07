from flask import Flask
from routes.ui import ui_bp
from routes.network import network_bp
from routes.actions import actions_bp
from routes.logs import logs_bp

app = Flask(__name__)

app.register_blueprint(ui_bp)
app.register_blueprint(network_bp)
app.register_blueprint(actions_bp)
app.register_blueprint(logs_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
