def test_health_endpoint(client):
    # Hacemos una petición GET a la ruta
    response = client.get("/health")
    
    # Verificamos que el servidor responda OK (200)
    assert response.status_code == 200
    # Verificamos que el JSON devuelto sea exactamente el esperado
    assert response.json == {"status": "ok"}