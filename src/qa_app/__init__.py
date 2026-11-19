from flask import Flask


def create_app():
    app = Flask(__name__)

    # Importamos y registramos el blueprint de salud
    from qa_app.api.health import health_bp
    from qa_app.web.questions import questions_bp

    app.register_blueprint(health_bp)
    app.extensions["qa_questions"] = {"items": [], "next_id": 1}
    app.register_blueprint(questions_bp)

    return app
