"""Instancias unicas das extensoes Flask, inicializadas no app factory."""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()
migrate = Migrate()


@event.listens_for(Engine, "connect")
def _ativar_integridade_sqlite(connection, _record):
    """Garante que SQLite respeite as Foreign Keys em desenvolvimento."""
    if connection.__class__.__module__.startswith("sqlite"):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
