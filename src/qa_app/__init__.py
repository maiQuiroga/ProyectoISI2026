from pathlib import Path

from flask import Flask

from qa_app.config import Config
from qa_app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.from_object(Config)
    if test_config is not None:
        app.config.update(test_config)

    # Importamos y registramos el blueprint de salud
    from qa_app.api.health import health_bp
    from qa_app.web.questions import questions_bp

    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(questions_bp)

    return app
