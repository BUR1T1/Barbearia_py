"""Model da entidade Barbeiro."""

from app.extensions import db


class Barbeiro(db.Model):
    __tablename__ = "barbeiros"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    especialidade = db.Column(db.String(100), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    agendamentos = db.relationship(
        "Agendamento", back_populates="barbeiro", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Barbeiro {self.id} {self.nome!r}>"
