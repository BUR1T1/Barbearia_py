"""Tratadores globais de erro -> todas as respostas de erro saem em JSON."""

from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.extensions import db
from app.errors.exceptions import ErroAPI


def registrar_tratadores_de_erro(app):
    @app.errorhandler(ErroAPI)
    def _erro_api(erro):
        return {"error": erro.mensagem}, erro.status

    @app.errorhandler(ValidationError)
    def _erro_validacao(erro):
        # 422: erro de validacao/tipagem no payload
        return {"error": "Erro de validacao no payload", "detalhes": erro.messages}, 422

    @app.errorhandler(404)
    def _nao_encontrado(_erro):
        return {"error": "Recurso nao encontrado"}, 404

    @app.errorhandler(405)
    def _metodo_nao_permitido(_erro):
        return {"error": "Metodo HTTP nao permitido para esta rota"}, 405

    @app.errorhandler(HTTPException)
    def _erro_http(erro):
        # cobre 400 (JSON invalido) e demais erros HTTP
        return {"error": erro.description}, erro.code

    @app.errorhandler(Exception)
    def _erro_interno(erro):
        db.session.rollback()
        app.logger.exception("Erro interno nao tratado: %s", erro)
        return {"error": "Erro interno do servidor"}, 500
