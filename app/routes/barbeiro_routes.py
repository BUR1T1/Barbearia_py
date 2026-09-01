"""Rotas HTTP da entidade Barbeiro.

Cada rota interpreta a requisicao, chama a camada de servico e devolve
a resposta com o status code correto.
"""

from flask import Blueprint, jsonify, request

from app.errors.exceptions import ErroAPI
from app.schemas.barbeiro_schema import esquema_barbeiro, esquema_barbeiros
from app.services import barbeiro_service

barbeiro_bp = Blueprint("barbeiros", __name__, url_prefix="/barbeiros")


def _corpo_json():
    """Retorna o corpo JSON da requisicao ou levanta 400 se ausente/invalido."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ErroAPI("O corpo da requisicao deve ser um JSON valido", 400)
    return dados


@barbeiro_bp.get("")
def listar_barbeiros():
    paginacao = barbeiro_service.listar_barbeiros(request.args)
    return jsonify(
        {
            "dados": esquema_barbeiros.dump(paginacao.items),
            "paginacao": {
                "pagina": paginacao.page,
                "por_pagina": paginacao.per_page,
                "total": paginacao.total,
                "total_paginas": paginacao.pages,
            },
        }
    ), 200


@barbeiro_bp.get("/<int:barbeiro_id>")
def detalhar_barbeiro(barbeiro_id):
    barbeiro = barbeiro_service.obter_barbeiro(barbeiro_id)
    return esquema_barbeiro.dump(barbeiro), 200


@barbeiro_bp.post("")
def criar_barbeiro():
    dados = esquema_barbeiro.load(_corpo_json())
    barbeiro = barbeiro_service.criar_barbeiro(dados)
    return esquema_barbeiro.dump(barbeiro), 201


@barbeiro_bp.put("/<int:barbeiro_id>")
def substituir_barbeiro(barbeiro_id):
    dados = esquema_barbeiro.load(_corpo_json())
    barbeiro = barbeiro_service.atualizar_barbeiro(barbeiro_id, dados)
    return esquema_barbeiro.dump(barbeiro), 200


@barbeiro_bp.patch("/<int:barbeiro_id>")
def atualizar_barbeiro_parcial(barbeiro_id):
    dados = esquema_barbeiro.load(_corpo_json(), partial=True)
    if not dados:
        raise ErroAPI("Informe ao menos um campo para atualizar", 400)
    barbeiro = barbeiro_service.atualizar_barbeiro(barbeiro_id, dados)
    return esquema_barbeiro.dump(barbeiro), 200


@barbeiro_bp.delete("/<int:barbeiro_id>")
def remover_barbeiro(barbeiro_id):
    barbeiro_service.remover_barbeiro(barbeiro_id)
    return "", 204
