"""Esquema de validacao e serializacao da entidade Servico (Marshmallow).

- ``load``  valida o corpo da requisicao (erro -> 422).
- ``dump``  converte o model em JSON de saida.
- PATCH usa ``load(..., partial=True)`` para deixar todos os campos opcionais.
"""

from marshmallow import EXCLUDE, Schema, fields, validate


class EsquemaServico(Schema):
    class Meta:
        unknown = EXCLUDE  # ignora campos extras enviados no corpo

    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    descricao = fields.Str(required=False, allow_none=True, validate=validate.Length(max=255))
    preco = fields.Decimal(required=True, as_string=True, places=2, validate=validate.Range(min=0.01))
    duracao_min = fields.Int(required=False, allow_none=True, validate=validate.Range(min=1))


esquema_servico = EsquemaServico()
esquema_servicos = EsquemaServico(many=True)
