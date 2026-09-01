"""Fabrica da aplicacao (app factory) da API da Barbearia."""

import os

from flask import Flask, jsonify

from config import Configuracao
from app.extensions import db, migrate
from app.errors.handlers import registrar_tratadores_de_erro


def criar_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Configuracao)

    os.makedirs(app.instance_path, exist_ok=True)

    # Extensoes
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa os models para o SQLAlchemy / Flask-Migrate reconhecerem as tabelas
    from app import models  # noqa: F401

    # Blueprints (uma entidade por membro do grupo)
    from app.routes.cliente_routes import cliente_bp
    from app.routes.barbeiro_routes import barbeiro_bp
    from app.routes.docs_routes import docs_bp

    app.register_blueprint(cliente_bp)
    app.register_blueprint(barbeiro_bp)
    app.register_blueprint(docs_bp)
    # TODO (Membro 3): app.register_blueprint(servico_bp)
    # TODO (Membro 4): app.register_blueprint(agendamento_bp)

    # Tratamento global de erros -> respostas JSON padronizadas
    registrar_tratadores_de_erro(app)

    @app.get("/")
    def inicio():
        return jsonify(
            {
                "api": "Barbearia",
                "versao": "1.0.0",
                "docs": "/docs",
                "openapi": "/openapi.json",
                "recursos": ["/clientes", "/barbeiros"],
            }
        )

    @app.cli.command("criar-banco")
    def criar_banco():
        """Cria as tabelas no banco (atalho para desenvolvimento)."""
        db.create_all()
        print("Banco criado em:", app.config["SQLALCHEMY_DATABASE_URI"])

    return app
