"""Validacao e serializacao de agendamentos."""

from marshmallow import EXCLUDE, Schema, fields, validate

from app.schemas.barbeiro_schema import EsquemaBarbeiro
from app.schemas.cliente_schema import EsquemaCliente
from app.schemas.servico_schema import EsquemaServico


class EsquemaAgendamento(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    data_hora = fields.DateTime(required=True)
    status = fields.Str(load_default="agendado", validate=validate.OneOf(["agendado", "concluido", "cancelado"]))
    observacao = fields.Str(allow_none=True, validate=validate.Length(max=255))
    cliente_id = fields.Int(required=True, validate=validate.Range(min=1))
    barbeiro_id = fields.Int(required=True, validate=validate.Range(min=1))
    servico_ids = fields.List(fields.Int(validate=validate.Range(min=1)), required=True, validate=validate.Length(min=1), load_only=True)
    cliente = fields.Nested(EsquemaCliente, dump_only=True)
    barbeiro = fields.Nested(EsquemaBarbeiro, dump_only=True)
    servicos = fields.Nested(EsquemaServico, many=True, dump_only=True)


esquema_agendamento = EsquemaAgendamento()
esquema_agendamentos = EsquemaAgendamento(many=True)
