def test_criar_servico(client):

    response = client.post(
        "/servicos",
        json={
            "nome": "Barba",
            "preco": "40.00"
        }
    )

    assert response.status_code == 201

    body = response.get_json()

    assert body["nome"] == "Barba"


def test_listar_servicos(client):

    response = client.get("/servicos")

    assert response.status_code == 200


def test_detalhar_servico(client):

    criado = client.post(
        "/servicos",
        json={
            "nome": "Corte Premium",
            "preco": "80.00"
        }
    ).get_json()

    response = client.get(
        f"/servicos/{criado['id']}"
    )

    assert response.status_code == 200


def test_servico_inexistente(client):

    response = client.get("/servicos/9999")

    assert response.status_code == 404


def test_servico_payload_invalido(client):

    response = client.post(
        "/servicos",
        json={
            "nome": "Corte",
            "preco": "0"
        }
    )

    assert response.status_code == 422
