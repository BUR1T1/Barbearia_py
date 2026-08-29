"""Camada de servico da entidade Cliente: regras de negocio e acesso ao banco.

As rotas nao usam o ``db`` diretamente; elas chamam estas funcoes.
"""

from app.extensions import db
from app.models.cliente import Cliente
from app.errors.exceptions import ErroAPI, NaoEncontrado

MAX_POR_PAGINA = 100


def listar_clientes(args):
    """Lista clientes com filtros e paginacao simples.

    Query string: ``nome``, ``email`` (busca parcial), ``page``, ``per_page``.
    """
    query = Cliente.query

    nome = args.get("nome")
    if nome:
        query = query.filter(Cliente.nome.ilike(f"%{nome}%"))

    email = args.get("email")
    if email:
        query = query.filter(Cliente.email.ilike(f"%{email}%"))

    try:
        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 10))
    except (TypeError, ValueError):
        raise ErroAPI("Parametros de paginacao devem ser numeros inteiros", 400)

    page = max(page, 1)
    per_page = min(max(per_page, 1), MAX_POR_PAGINA)

    return query.order_by(Cliente.id).paginate(
        page=page, per_page=per_page, error_out=False
    )


def obter_cliente(cliente_id):
    cliente = db.session.get(Cliente, cliente_id)
    if cliente is None:
        raise NaoEncontrado(f"Cliente com id {cliente_id} nao encontrado")
    return cliente


def criar_cliente(dados):
    cliente = Cliente(**dados)
    db.session.add(cliente)
    db.session.commit()
    return cliente


def atualizar_cliente(cliente_id, dados):
    """Serve para PUT (payload completo) e PATCH (payload parcial)."""
    cliente = obter_cliente(cliente_id)
    for campo, valor in dados.items():
        setattr(cliente, campo, valor)
    db.session.commit()
    return cliente


def remover_cliente(cliente_id):
    cliente = obter_cliente(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
