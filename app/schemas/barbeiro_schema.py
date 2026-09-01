"""Esquema de validacao e serializacao da entidade Barbeiro (Marshmallow).

- ``load``  valida o corpo da requisicao (erro -> 422).
- ``dump``  converte o model em JSON de saida.
- PATCH usa ``load(..., partial=True)`` para deixar todos os campos opcionais.
"""

from marshmallow import EXCLUDE, Schema, fields, validate


class EsquemaBarbeiro(Schema):
    class Meta:
        unknown = EXCLUDE  # ignora campos extras enviados no corpo

    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    especialidade = fields.Str(required=False, allow_none=True, validate=validate.Length(max=100))
    telefone = fields.Str(required=False, allow_none=True, validate=validate.Length(min=8, max=20))
    ativo = fields.Bool(load_default=True)


esquema_barbeiro = EsquemaBarbeiro()
esquema_barbeiros = EsquemaBarbeiro(many=True)
