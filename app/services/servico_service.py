"""Camada de servico da entidade Servico: regras de negocio e acesso ao banco.

As rotas nao usam o ``db`` diretamente; elas chamam estas funcoes.
"""

from decimal import Decimal, InvalidOperation

from app.extensions import db
from app.models.servico import Servico
from app.errors.exceptions import ErroAPI, NaoEncontrado

MAX_POR_PAGINA = 100


def _preco_do_filtro(args, chave):
    """Converte um filtro de preco da query string em Decimal (ou None)."""
    valor = args.get(chave)
    if valor is None or str(valor).strip() == "":
        return None
    try:
        return Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        raise ErroAPI(f"Parametro '{chave}' deve ser um numero valido", 400)


def listar_servicos(args):
    """Lista servicos com filtros e paginacao simples.

    Query string: ``nome`` (busca parcial), ``preco_min``, ``preco_max``,
    ``page``, ``per_page``.
    """
    query = Servico.query

    nome = args.get("nome")
    if nome:
        query = query.filter(Servico.nome.ilike(f"%{nome}%"))

    preco_min = _preco_do_filtro(args, "preco_min")
    if preco_min is not None:
        query = query.filter(Servico.preco >= preco_min)

    preco_max = _preco_do_filtro(args, "preco_max")
    if preco_max is not None:
        query = query.filter(Servico.preco <= preco_max)

    try:
        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 10))
    except (TypeError, ValueError):
        raise ErroAPI("Parametros de paginacao devem ser numeros inteiros", 400)

    page = max(page, 1)
    per_page = min(max(per_page, 1), MAX_POR_PAGINA)

    return query.order_by(Servico.id).paginate(
        page=page, per_page=per_page, error_out=False
    )


def obter_servico(servico_id):
    servico = db.session.get(Servico, servico_id)
    if servico is None:
        raise NaoEncontrado(f"Servico com id {servico_id} nao encontrado")
    return servico


def criar_servico(dados):
    servico = Servico(**dados)
    db.session.add(servico)
    db.session.commit()
    return servico


def atualizar_servico(servico_id, dados):
    """Serve para PUT (payload completo) e PATCH (payload parcial)."""
    servico = obter_servico(servico_id)
    for campo, valor in dados.items():
        setattr(servico, campo, valor)
    db.session.commit()
    return servico


def remover_servico(servico_id):
    servico = obter_servico(servico_id)
    db.session.delete(servico)
    db.session.commit()
