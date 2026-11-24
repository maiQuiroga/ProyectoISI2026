def register_user(client):
    return client.post(
        "/register",
        data={
            "name": "Usuario de prueba",
            "email": "qa@example.com",
            "password": "password-segura",
        },
    )


def test_question_and_answer_flow(client):
    assert register_user(client).status_code == 302
    created = client.post(
        "/questions",
        data={
            "title": "Consulta Flask",
            "category": "Flask",
            "body": "¿Cómo registro las rutas?",
            "tags": "python, flask",
        },
    )

    assert created.status_code == 302
    detail_url = created.headers["Location"]
    detail = client.get(detail_url)
    assert detail.status_code == 200
    assert b"Consulta Flask" in detail.data
    assert b"python" in detail.data

    listing = client.get("/")
    assert b"Consulta Flask" in listing.data

    answered = client.post(
        f"{detail_url}/responses", data={"body": "Con un blueprint."}
    )
    assert answered.status_code == 302
    detail = client.get(detail_url)
    assert b"Con un blueprint." in detail.data
    assert b"Usuario" in detail.data


def test_invalid_forms_and_missing_question(client):
    assert register_user(client).status_code == 302
    assert client.post("/questions", data={}).status_code == 400
    assert client.post(
        "/questions",
        data={"title": "Pregunta", "category": "Otra", "body": "Detalle"},
    ).status_code == 400
    assert client.get("/questions/no-existe").status_code == 404
    assert client.post(
        "/questions/no-existe/responses", data={"body": "Respuesta"}
    ).status_code == 404

    created = client.post(
        "/questions",
        data={"title": "Pregunta", "category": "Flask", "body": "Detalle"},
    )
    assert client.post(
        f"{created.headers['Location']}/responses", data={"body": "  "}
    ).status_code == 400


def test_ia_help_tag_creates_ai_answer(client,monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert register_user(client).status_code == 302
    created = client.post(
        "/questions",
        data={
            "title": "Pregunta asistida",
            "category": "Python",
            "body": "¿Cómo organizar el flujo?",
            "tags": "#ia-help",
        },
    )

    assert created.status_code == 302
    detail = client.get(created.headers["Location"])
    assert detail.status_code == 200
    assert b"[Agente IA]" in detail.data
    assert b"Gemini simulado" in detail.data
