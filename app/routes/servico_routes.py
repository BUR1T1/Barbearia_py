"""Rotas HTTP da entidade Servico.

Cada rota interpreta a requisicao, chama a camada de servico e devolve
a resposta com o status code correto.
"""

from flask import Blueprint, jsonify, request

from app.errors.exceptions import ErroAPI
from app.schemas.servico_schema import esquema_servico, esquema_servicos
from app.services import servico_service

servico_bp = Blueprint("servicos", __name__, url_prefix="/servicos")


def _corpo_json():
    """Retorna o corpo JSON da requisicao ou levanta 400 se ausente/invalido."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ErroAPI("O corpo da requisicao deve ser um JSON valido", 400)
    return dados


@servico_bp.get("")
def listar_servicos():
    paginacao = servico_service.listar_servicos(request.args)
    return jsonify(
        {
            "dados": esquema_servicos.dump(paginacao.items),
            "paginacao": {
                "pagina": paginacao.page,
                "por_pagina": paginacao.per_page,
                "total": paginacao.total,
                "total_paginas": paginacao.pages,
            },
        }
    ), 200


@servico_bp.get("/<int:servico_id>")
def detalhar_servico(servico_id):
    servico = servico_service.obter_servico(servico_id)
    return esquema_servico.dump(servico), 200


@servico_bp.post("")
def criar_servico():
    dados = esquema_servico.load(_corpo_json())
    servico = servico_service.criar_servico(dados)
    return esquema_servico.dump(servico), 201


@servico_bp.put("/<int:servico_id>")
def substituir_servico(servico_id):
    dados = esquema_servico.load(_corpo_json())
    servico = servico_service.atualizar_servico(servico_id, dados)
    return esquema_servico.dump(servico), 200


@servico_bp.patch("/<int:servico_id>")
def atualizar_servico_parcial(servico_id):
    dados = esquema_servico.load(_corpo_json(), partial=True)
    if not dados:
        raise ErroAPI("Informe ao menos um campo para atualizar", 400)
    servico = servico_service.atualizar_servico(servico_id, dados)
    return esquema_servico.dump(servico), 200


@servico_bp.delete("/<int:servico_id>")
def remover_servico(servico_id):
    servico_service.remover_servico(servico_id)
    return "", 204
