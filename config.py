"""Configuracao da aplicacao, lida de variaveis de ambiente (.env)."""

import os

from dotenv import load_dotenv

DIRETORIO_BASE = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(DIRETORIO_BASE, ".env"))


class Configuracao:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-de-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(DIRETORIO_BASE, "instance", "barbearia.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
