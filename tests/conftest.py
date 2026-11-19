import pytest

from qa_app import create_app


@pytest.fixture
def app():
    # Instanciamos la app usando la factory que creaste
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    # Creamos un cliente de prueba para simular peticiones del navegador
    return app.test_client()