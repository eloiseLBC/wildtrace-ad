import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

FLASK_LOG_FILE = Path(__file__).resolve().parents[1] / 'logs' / 'flask.log'


def configure_logging(app):
    FLASK_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        FLASK_LOG_FILE, maxBytes=2_000_000, backupCount=3, encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s: %(message)s'
    ))
    for logger in (app.logger, logging.getLogger('werkzeug')):
        if not any(isinstance(h, RotatingFileHandler)
                   and h.baseFilename == str(FLASK_LOG_FILE) for h in logger.handlers):
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    app.logger.info('WildTrace admin démarré')
