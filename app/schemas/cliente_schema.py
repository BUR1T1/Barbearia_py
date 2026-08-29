"""Esquema de validacao e serializacao da entidade Cliente (Marshmallow).

- ``load``  valida o corpo da requisicao (erro -> 422).
- ``dump``  converte o model em JSON de saida.
- PATCH usa ``load(..., partial=True)`` para deixar todos os campos opcionais.
"""

from marshmallow import EXCLUDE, Schema, fields, validate


class EsquemaCliente(Schema):
    class Meta:
        unknown = EXCLUDE  # ignora campos extras enviados no corpo

    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    telefone = fields.Str(required=True, validate=validate.Length(min=8, max=20))
    email = fields.Email(required=False, allow_none=True)
    data_cadastro = fields.DateTime(dump_only=True)


esquema_cliente = EsquemaCliente()
esquema_clientes = EsquemaCliente(many=True)
