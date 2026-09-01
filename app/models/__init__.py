"""Agrega os models para que Flask-Migrate detecte todas as tabelas.

Cada membro deve importar aqui o seu model ao cria-lo.
"""

from app.models.cliente import Cliente  # noqa: F401
from app.models.barbeiro import Barbeiro  # noqa: F401

# TODO (Membro 3): from app.models.servico import Servico
# TODO (Membro 4): from app.models.agendamento import Agendamento
