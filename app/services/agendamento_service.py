"""Regras de negocio e persistencia de agendamentos."""

from app.extensions import db
from app.errors.exceptions import ErroAPI, NaoEncontrado
from app.models.agendamento import Agendamento
from app.models.barbeiro import Barbeiro
from app.models.cliente import Cliente
from app.models.servico import Servico

MAX_POR_PAGINA = 100


def _referencias(dados):
    cliente = db.session.get(Cliente, dados["cliente_id"])
    barbeiro = db.session.get(Barbeiro, dados["barbeiro_id"])
    servicos = db.session.scalars(db.select(Servico).where(Servico.id.in_(dados["servico_ids"]))).all()
    if cliente is None or barbeiro is None or len(servicos) != len(set(dados["servico_ids"])):
        raise ErroAPI("Cliente, barbeiro e servicos informados devem existir", 422)
    return servicos


def listar_agendamentos(args):
    query = Agendamento.query
    for campo, modelo in (("cliente_id", Agendamento.cliente_id), ("barbeiro_id", Agendamento.barbeiro_id)):
        if args.get(campo) is not None:
            try:
                query = query.filter(modelo == int(args[campo]))
            except (TypeError, ValueError):
                raise ErroAPI(f"Parametro '{campo}' deve ser inteiro", 400)
    if args.get("status"):
        if args["status"] not in ("agendado", "concluido", "cancelado"):
            raise ErroAPI("Parametro 'status' invalido", 400)
        query = query.filter(Agendamento.status == args["status"])
    try:
        page = max(int(args.get("page", 1)), 1)
        per_page = min(max(int(args.get("per_page", 10)), 1), MAX_POR_PAGINA)
    except (TypeError, ValueError):
        raise ErroAPI("Parametros de paginacao devem ser numeros inteiros", 400)
    return query.order_by(Agendamento.data_hora, Agendamento.id).paginate(page=page, per_page=per_page, error_out=False)


def obter_agendamento(agendamento_id):
    agendamento = db.session.get(Agendamento, agendamento_id)
    if agendamento is None:
        raise NaoEncontrado(f"Agendamento com id {agendamento_id} nao encontrado")
    return agendamento


def criar_agendamento(dados):
    servicos = _referencias(dados)
    dados = dict(dados)
    dados.pop("servico_ids")
    agendamento = Agendamento(**dados, servicos=servicos)
    db.session.add(agendamento)
    db.session.commit()
    return agendamento


def atualizar_agendamento(agendamento_id, dados):
    agendamento = obter_agendamento(agendamento_id)
    dados = dict(dados)
    servico_ids = dados.pop("servico_ids", None)
    if servico_ids is not None or "cliente_id" in dados or "barbeiro_id" in dados:
        referencias = _referencias({
            "cliente_id": dados.get("cliente_id", agendamento.cliente_id),
            "barbeiro_id": dados.get("barbeiro_id", agendamento.barbeiro_id),
            "servico_ids": servico_ids if servico_ids is not None else [servico.id for servico in agendamento.servicos],
        })
        if servico_ids is not None:
            agendamento.servicos = referencias
    for campo, valor in dados.items():
        setattr(agendamento, campo, valor)
    db.session.commit()
    return agendamento


def remover_agendamento(agendamento_id):
    agendamento = obter_agendamento(agendamento_id)
    db.session.delete(agendamento)
    db.session.commit()
