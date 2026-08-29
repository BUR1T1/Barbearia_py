"""Erros de negocio da API.

A camada de servico levanta estes erros; os tratadores em ``handlers.py``
transformam cada um em uma resposta JSON com o status HTTP correto.
"""


class ErroAPI(Exception):
    """Erro previsto da API. Vira ``{"error": <mensagem>}`` com o status informado."""

    status = 400

    def __init__(self, mensagem, status=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        if status is not None:
            self.status = status


class NaoEncontrado(ErroAPI):
    """Recurso ou identificador inexistente -> 404."""

    def __init__(self, mensagem="Recurso nao encontrado"):
        super().__init__(mensagem, 404)
