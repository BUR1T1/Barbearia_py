"""Rotas de documentacao interativa Swagger / OpenAPI."""

from flask import Blueprint, jsonify, redirect, render_template_string

from app.docs.swagger_spec import OPENAPI_SPEC

docs_bp = Blueprint("docs", __name__)

SWAGGER_UI_HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Documentação Swagger - API Barbearia</title>
  <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
  <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@5/favicon-32x32.png" sizes="32x32" />
  <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@5/favicon-16x16.png" sizes="16x16" />
  <style>
    html {
      box-sizing: border-box;
      overflow: -moz-scrollbars-vertical;
      overflow-y: scroll;
    }
    *, *:before, *:after {
      box-sizing: inherit;
    }
    body {
      margin: 0;
      background: #fafafa;
    }
    .topbar {
      display: none;
    }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js" charset="UTF-8"></script>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js" charset="UTF-8"></script>
  <script>
    window.onload = function() {
      window.ui = SwaggerUIBundle({
        url: "/openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: "StandaloneLayout"
      });
    };
  </script>
</body>
</html>
"""


@docs_bp.get("/openapi.json")
def obter_especificacao_openapi():
    """Retorna o documento JSON da especificacao OpenAPI 3.0."""
    return jsonify(OPENAPI_SPEC), 200


@docs_bp.get("/docs")
def renderizar_swagger_ui():
    """Renderiza a interface grafica do Swagger UI."""
    return render_template_string(SWAGGER_UI_HTML), 200


@docs_bp.get("/swagger")
def redirecionar_swagger():
    """Redireciona /swagger para /docs."""
    return redirect("/docs"), 302
