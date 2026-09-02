"""Model da entidade Servico."""

from app.extensions import db


class Servico(db.Model):
    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    duracao_min = db.Column(db.Integer, nullable=True)

    # Relacionamento N:N com Agendamento -> a TODO do Membro 4 adiciona aqui:
    # agendamentos = db.relationship(
    #     "Agendamento", secondary="agendamento_servicos", back_populates="servicos"
    # )

    def __repr__(self):
        return f"<Servico {self.id} {self.nome!r}>"
