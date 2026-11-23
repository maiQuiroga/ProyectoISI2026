from pathlib import Path

import click
from flask import Flask
from sqlalchemy import select
from sqlalchemy.engine import make_url
from werkzeug.security import generate_password_hash

from qa_app.config import Config
from qa_app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.from_object(Config)
    if test_config is not None:
        app.config.update(test_config)

    database_url = make_url(app.config["SQLALCHEMY_DATABASE_URI"])
    if database_url.get_backend_name() == "sqlite" and database_url.database not in (
        None,
        ":memory:",
    ):
        Path(database_url.database).expanduser().resolve().parent.mkdir(
            parents=True, exist_ok=True
        )

    # Importamos y registramos el blueprint de salud
    from qa_app.api.health import health_bp
    from qa_app.models import HumanUser, RoleType
    from qa_app.web.auth import auth_bp, get_current_user
    from qa_app.web.questions import questions_bp

    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(questions_bp)

    @app.context_processor
    def inject_current_user():
        return {"current_user": get_current_user()}

    @app.cli.command("create-admin")
    @click.argument("email")
    def create_admin(email):
        """Crear un administrador o promover una cuenta existente."""
        normalized_email = email.strip().lower()
        user = db.session.scalar(
            select(HumanUser).where(HumanUser.email == normalized_email)
        )
        if user is None:
            name = click.prompt("Nombre")
            password = click.prompt(
                "Contraseña (mínimo 8 caracteres)",
                hide_input=True,
                confirmation_prompt=True,
            )
            if not name.strip() or len(password) < 8:
                raise click.ClickException(
                    "El nombre es obligatorio y la contraseña debe tener 8 caracteres."
                )
            user = HumanUser(
                name=name.strip(),
                email=normalized_email,
                password_hash=generate_password_hash(password),
            )
            db.session.add(user)

        user.role = RoleType.ADMIN
        db.session.commit()
        click.echo(f"La cuenta {normalized_email} tiene rol Admin.")

    return app
