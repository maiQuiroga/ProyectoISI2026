from qa_app import create_app


def test_health_endpoint(client):
    # Hacemos una petición GET a la ruta
    response = client.get("/health")

    # Verificamos que el servidor responda OK (200)
    assert response.status_code == 200
    # Verificamos que el JSON devuelto sea exactamente el esperado
    assert response.json == {"status": "ok"}


def test_app_creates_parent_directory_for_sqlite_database(tmp_path):
    database_path = tmp_path / "not-created-yet" / "nested" / "qa.db"
    create_app(
        {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}"}
    )

    assert database_path.parent.is_dir()
