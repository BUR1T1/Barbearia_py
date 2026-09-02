"""Rotas REST de agendamentos."""

from flask import Blueprint, jsonify, request
from app.errors.exceptions import ErroAPI
from app.schemas.agendamento_schema import esquema_agendamento, esquema_agendamentos
from app.services import agendamento_service

agendamento_bp = Blueprint("agendamentos", __name__, url_prefix="/agendamentos")


def _corpo_json():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ErroAPI("O corpo da requisicao deve ser um JSON valido", 400)
    return dados


@agendamento_bp.get("")
def listar_agendamentos():
    pagina = agendamento_service.listar_agendamentos(request.args)
    return jsonify({"dados": esquema_agendamentos.dump(pagina.items), "paginacao": {"pagina": pagina.page, "por_pagina": pagina.per_page, "total": pagina.total, "total_paginas": pagina.pages}}), 200


@agendamento_bp.get("/<int:agendamento_id>")
def detalhar_agendamento(agendamento_id):
    return esquema_agendamento.dump(agendamento_service.obter_agendamento(agendamento_id)), 200


@agendamento_bp.post("")
def criar_agendamento():
    return esquema_agendamento.dump(agendamento_service.criar_agendamento(esquema_agendamento.load(_corpo_json()))), 201


@agendamento_bp.put("/<int:agendamento_id>")
def substituir_agendamento(agendamento_id):
    dados = esquema_agendamento.load(_corpo_json())
    return esquema_agendamento.dump(agendamento_service.atualizar_agendamento(agendamento_id, dados)), 200


@agendamento_bp.patch("/<int:agendamento_id>")
def atualizar_agendamento_parcial(agendamento_id):
    dados = esquema_agendamento.load(_corpo_json(), partial=True)
    if not dados:
        raise ErroAPI("Informe ao menos um campo para atualizar", 400)
    return esquema_agendamento.dump(agendamento_service.atualizar_agendamento(agendamento_id, dados)), 200


@agendamento_bp.delete("/<int:agendamento_id>")
def remover_agendamento(agendamento_id):
    agendamento_service.remover_agendamento(agendamento_id)
    return "", 204
