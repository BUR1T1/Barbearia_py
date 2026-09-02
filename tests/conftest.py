import pytest

from app import criar_app
from app.extensions import db


@pytest.fixture()
def client(tmp_path):
    app = criar_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'teste.db'}"})
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as test_client:
        yield test_client
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def dados_base(client):
    cliente = client.post("/clientes", json={"nome": "Ana Cliente", "telefone": "11999999999"}).get_json()
    barbeiro = client.post("/barbeiros", json={"nome": "Bruno Barbeiro"}).get_json()
    servico = client.post("/servicos", json={"nome": "Corte", "preco": "50.00"}).get_json()
    return cliente, barbeiro, servico
