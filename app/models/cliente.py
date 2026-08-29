"""Model da entidade Cliente."""

from datetime import datetime, timezone

from app.extensions import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    data_cadastro = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Relacionamento 1:N com Agendamento -> a TODO do Membro 4 adiciona aqui:
    # agendamentos = db.relationship(
    #     "Agendamento", back_populates="cliente", cascade="all, delete-orphan"
    # )

    def __repr__(self):
        return f"<Cliente {self.id} {self.nome!r}>"
