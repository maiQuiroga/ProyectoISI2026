from flask import Flask


def create_app():
    app = Flask(__name__)

    # Importamos y registramos el blueprint de salud
    from qa_app.api.health import health_bp
    app.register_blueprint(health_bp)

    return app