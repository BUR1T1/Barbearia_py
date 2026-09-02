def test_criar_barbeiro(client):

    response = client.post(
        "/barbeiros",
        json={
            "nome": "João Barbeiro",
            "telefone": "11988888888"
        }
    )

    assert response.status_code == 201

    body = response.get_json()

    assert body["nome"] == "João Barbeiro"


def test_listar_barbeiros(client):

    response = client.get("/barbeiros")

    assert response.status_code == 200


def test_detalhar_barbeiro(client):

    criado = client.post(
        "/barbeiros",
        json={
            "nome": "Carlos Barbeiro"
        }
    ).get_json()

    response = client.get(
        f"/barbeiros/{criado['id']}"
    )

    assert response.status_code == 200


def test_barbeiro_inexistente(client):

    response = client.get("/barbeiros/9999")

    assert response.status_code == 404


def test_barbeiro_payload_invalido(client):

    response = client.post(
        "/barbeiros",
        json={
            "nome": ""
        }
    )

    assert response.status_code == 422
