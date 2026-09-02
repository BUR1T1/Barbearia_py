"""Modelos de agendamento e da associacao N:N com servicos."""

from app.extensions import db


agendamento_servicos = db.Table(
    "agendamento_servicos",
    db.Column("agendamento_id", db.Integer, db.ForeignKey("agendamentos.id", ondelete="CASCADE"), primary_key=True),
    db.Column("servico_id", db.Integer, db.ForeignKey("servicos.id", ondelete="RESTRICT"), primary_key=True),
)


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="agendado")
    observacao = db.Column(db.String(255), nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id", ondelete="RESTRICT"), nullable=False)
    barbeiro_id = db.Column(db.Integer, db.ForeignKey("barbeiros.id", ondelete="RESTRICT"), nullable=False)

    cliente = db.relationship("Cliente", back_populates="agendamentos")
    barbeiro = db.relationship("Barbeiro", back_populates="agendamentos")
    servicos = db.relationship("Servico", secondary=agendamento_servicos, back_populates="agendamentos")

    def __repr__(self):
        return f"<Agendamento {self.id} {self.data_hora!r}>"
