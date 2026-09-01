"""Camada de servico da entidade Barbeiro: regras de negocio e acesso ao banco.

As rotas nao usam o ``db`` diretamente; elas chamam estas funcoes.
"""

from app.extensions import db
from app.models.barbeiro import Barbeiro
from app.errors.exceptions import ErroAPI, NaoEncontrado

MAX_POR_PAGINA = 100


def listar_barbeiros(args):
    """Lista barbeiros com filtros e paginacao simples.

    Query string: ``nome`` (busca parcial), ``ativo`` (booleano), ``page``, ``per_page``.
    """
    query = Barbeiro.query

    nome = args.get("nome")
    if nome:
        query = query.filter(Barbeiro.nome.ilike(f"%{nome}%"))

    ativo = args.get("ativo")
    if ativo is not None:
        ativo_str = str(ativo).strip().lower()
        if ativo_str in ("true", "1", "t", "sim", "s"):
            query = query.filter(Barbeiro.ativo.is_(True))
        elif ativo_str in ("false", "0", "f", "nao", "n"):
            query = query.filter(Barbeiro.ativo.is_(False))
        else:
            raise ErroAPI("Parametro 'ativo' deve ser um booleano valido (true ou false)", 400)

    try:
        page = int(args.get("page", 1))
        per_page = int(args.get("per_page", 10))
    except (TypeError, ValueError):
        raise ErroAPI("Parametros de paginacao devem ser numeros inteiros", 400)

    page = max(page, 1)
    per_page = min(max(per_page, 1), MAX_POR_PAGINA)

    return query.order_by(Barbeiro.id).paginate(
        page=page, per_page=per_page, error_out=False
    )


def obter_barbeiro(barbeiro_id):
    barbeiro = db.session.get(Barbeiro, barbeiro_id)
    if barbeiro is None:
        raise NaoEncontrado(f"Barbeiro com id {barbeiro_id} nao encontrado")
    return barbeiro


def criar_barbeiro(dados):
    barbeiro = Barbeiro(**dados)
    db.session.add(barbeiro)
    db.session.commit()
    return barbeiro


def atualizar_barbeiro(barbeiro_id, dados):
    """Serve para PUT (payload completo) e PATCH (payload parcial)."""
    barbeiro = obter_barbeiro(barbeiro_id)
    for campo, valor in dados.items():
        setattr(barbeiro, campo, valor)
    db.session.commit()
    return barbeiro


def remover_barbeiro(barbeiro_id):
    barbeiro = obter_barbeiro(barbeiro_id)
    db.session.delete(barbeiro)
    db.session.commit()
