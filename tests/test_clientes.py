def test_criar_cliente(client):

    response = client.post(
        "/clientes",
        json={
            "nome": "Carlos Cliente",
            "telefone": "11988888888",
            "email": "carlos@email.com"
        }
    )

    assert response.status_code == 201

    body = response.get_json()

    assert body["nome"] == "Carlos Cliente"
    assert body["telefone"] == "11988888888"


def test_listar_clientes(client):

    client.post(
        "/clientes",
        json={
            "nome": "Ana",
            "telefone": "11999999999"
        }
    )

    response = client.get("/clientes")

    assert response.status_code == 200


def test_detalhar_cliente(client):

    criado = client.post(
        "/clientes",
        json={
            "nome": "Maria Cliente",
            "telefone": "11977777777"
        }
    ).get_json()

    response = client.get(
        f"/clientes/{criado['id']}"
    )

    assert response.status_code == 200


def test_cliente_inexistente(client):

    response = client.get("/clientes/9999")

    assert response.status_code == 404


def test_cliente_payload_invalido(client):

    response = client.post(
        "/clientes",
        json={
            "telefone": "123"
        }
    )

    assert response.status_code == 422
