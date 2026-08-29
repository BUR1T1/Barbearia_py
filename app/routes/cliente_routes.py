"""Rotas HTTP da entidade Cliente.

Cada rota interpreta a requisicao, chama a camada de servico e devolve
a resposta com o status code correto.
"""

from flask import Blueprint, jsonify, request

from app.errors.exceptions import ErroAPI
from app.schemas.cliente_schema import esquema_cliente, esquema_clientes
from app.services import cliente_service

cliente_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


def _corpo_json():
    """Retorna o corpo JSON da requisicao ou levanta 400 se ausente/invalido."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ErroAPI("O corpo da requisicao deve ser um JSON valido", 400)
    return dados


@cliente_bp.get("")
def listar_clientes():
    paginacao = cliente_service.listar_clientes(request.args)
    return jsonify(
        {
            "dados": esquema_clientes.dump(paginacao.items),
            "paginacao": {
                "pagina": paginacao.page,
                "por_pagina": paginacao.per_page,
                "total": paginacao.total,
                "total_paginas": paginacao.pages,
            },
        }
    ), 200


@cliente_bp.get("/<int:cliente_id>")
def detalhar_cliente(cliente_id):
    cliente = cliente_service.obter_cliente(cliente_id)
    return esquema_cliente.dump(cliente), 200


@cliente_bp.post("")
def criar_cliente():
    dados = esquema_cliente.load(_corpo_json())
    cliente = cliente_service.criar_cliente(dados)
    return esquema_cliente.dump(cliente), 201


@cliente_bp.put("/<int:cliente_id>")
def substituir_cliente(cliente_id):
    dados = esquema_cliente.load(_corpo_json())
    cliente = cliente_service.atualizar_cliente(cliente_id, dados)
    return esquema_cliente.dump(cliente), 200


@cliente_bp.patch("/<int:cliente_id>")
def atualizar_cliente_parcial(cliente_id):
    dados = esquema_cliente.load(_corpo_json(), partial=True)
    if not dados:
        raise ErroAPI("Informe ao menos um campo para atualizar", 400)
    cliente = cliente_service.atualizar_cliente(cliente_id, dados)
    return esquema_cliente.dump(cliente), 200


@cliente_bp.delete("/<int:cliente_id>")
def remover_cliente(cliente_id):
    cliente_service.remover_cliente(cliente_id)
    return "", 204
