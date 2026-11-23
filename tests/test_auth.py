from sqlalchemy import select
from werkzeug.security import check_password_hash

from qa_app.extensions import db
from qa_app.models import HumanUser, Question, RoleType


def register(client, email="user@example.com", password="password-segura"):
    return client.post(
        "/register",
        data={"name": "Usuario de prueba", "email": email, "password": password},
    )


def test_register_normalizes_email_and_assigns_general_role(client, app):
    response = register(client, "  USER@Example.COM  ")

    assert response.status_code == 302
    with app.app_context():
        user = db.session.scalar(
            select(HumanUser).where(HumanUser.email == "user@example.com")
        )
        assert user is not None
        assert user.role == RoleType.GENERAL_USER
        assert check_password_hash(user.password_hash, "password-segura")

    with client.session_transaction() as browser_session:
        assert browser_session["user_id"] == user.id


def test_register_rejects_duplicate_email_and_invalid_fields(client):
    assert register(client).status_code == 302
    duplicate = register(client, "USER@example.com")
    assert duplicate.status_code == 400
    assert b"ya est\xc3\xa1 registrado" in duplicate.data

    assert register(client, email="", password="password-segura").status_code == 400
    short_password = register(client, email="new@example.com", password="short")
    assert short_password.status_code == 400


def test_login_accepts_normalized_email_and_rejects_invalid_credentials(client):
    assert register(client).status_code == 302
    client.post("/logout")

    invalid = client.post(
        "/login", data={"email": "user@example.com", "password": "incorrecta"}
    )
    assert invalid.status_code == 401
    assert b"Correo o contrase\xc3\xb1a incorrectos" in invalid.data

    valid = client.post(
        "/login", data={"email": " USER@EXAMPLE.COM ", "password": "password-segura"}
    )
    assert valid.status_code == 302
    with client.session_transaction() as browser_session:
        assert "user_id" in browser_session


def test_logout_clears_session(client):
    assert register(client).status_code == 302
    response = client.post("/logout")

    assert response.status_code == 302
    with client.session_transaction() as browser_session:
        assert "user_id" not in browser_session


def test_anonymous_cannot_publish_or_answer(client):
    assert register(client).status_code == 302
    created = client.post(
        "/questions",
        data={"title": "Pregunta", "category": "Flask", "body": "Detalle"},
    )
    question_url = created.headers["Location"]
    client.post("/logout")

    response = client.post(
        "/questions",
        data={"title": "Pregunta", "category": "Flask", "body": "Detalle"},
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
    answer_response = client.post(
        f"{question_url}/responses", data={"body": "Respuesta"}
    )
    assert answer_response.status_code == 302
    assert answer_response.headers["Location"].endswith("/login")


def test_only_admin_can_delete_questions(client, app):
    assert register(client).status_code == 302
    created = client.post(
        "/questions",
        data={"title": "Pregunta", "category": "Flask", "body": "Detalle"},
    )
    question_url = created.headers["Location"]
    question_id = question_url.rsplit("/", 1)[-1]

    assert client.post(f"{question_url}/delete").status_code == 403

    with app.app_context():
        user = db.session.scalar(
            select(HumanUser).where(HumanUser.email == "user@example.com")
        )
        user.role = RoleType.ADMIN
        db.session.commit()

    admin_login = client.post(
        "/login", data={"email": "user@example.com", "password": "password-segura"}
    )
    assert admin_login.status_code == 302
    assert client.post(f"{question_url}/delete").status_code == 302

    with app.app_context():
        assert db.session.get(Question, question_id) is None


def test_create_admin_cli_creates_admin_user(app):
    result = app.test_cli_runner().invoke(
        args=["create-admin", "admin@example.com"],
        input="Administradora\npassword-segura\npassword-segura\n",
    )

    assert result.exit_code == 0, result.output
    with app.app_context():
        admin = db.session.scalar(
            select(HumanUser).where(HumanUser.email == "admin@example.com")
        )
        assert admin is not None
        assert admin.role == RoleType.ADMIN
