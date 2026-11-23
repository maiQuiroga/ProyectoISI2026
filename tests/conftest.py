import pytest

from qa_app import create_app
from qa_app.extensions import db


@pytest.fixture
def app():
    # Instanciamos la app usando la factory que creaste
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    # Creamos un cliente de prueba para simular peticiones del navegador
    return app.test_client()
