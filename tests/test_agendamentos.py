from datetime import datetime


def payload(dados_base):
    cliente, barbeiro, servico = dados_base
    return {
        "data_hora": datetime(2026, 9, 3, 14, 30).isoformat(),
        "cliente_id": cliente["id"],
        "barbeiro_id": barbeiro["id"],
        "servico_ids": [servico["id"]],
    }


def test_crud_agendamento_e_relacionamentos(client, dados_base):
    criado = client.post("/agendamentos", json=payload(dados_base))
    assert criado.status_code == 201
    body = criado.get_json()
    assert body["cliente"]["id"] == dados_base[0]["id"]
    assert body["barbeiro"]["id"] == dados_base[1]["id"]
    assert body["servicos"][0]["id"] == dados_base[2]["id"]

    agendamento_id = body["id"]
    assert client.get(f"/agendamentos/{agendamento_id}").status_code == 200
    assert client.patch(f"/agendamentos/{agendamento_id}", json={"status": "concluido"}).status_code == 200
    assert client.put(f"/agendamentos/{agendamento_id}", json=payload(dados_base)).status_code == 200
    assert client.delete(f"/agendamentos/{agendamento_id}").status_code == 204


def test_agendamento_valida_referencias_e_payload(client, dados_base):
    body = payload(dados_base)
    body["cliente_id"] = 9999
    assert client.post("/agendamentos", json=body).status_code == 422
    body = payload(dados_base)
    body["servico_ids"] = []
    assert client.post("/agendamentos", json=body).status_code == 422
    assert client.get("/agendamentos/9999").status_code == 404
