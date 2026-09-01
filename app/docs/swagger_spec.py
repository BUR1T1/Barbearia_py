"""Especificacao OpenAPI 3.0 para a API da Barbearia."""

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "API RESTful - Barbearia",
        "description": "API RESTful para gestão de barbearia com Flask, SQLAlchemy, Marshmallow e arquitetura em camadas.",
        "version": "1.0.0",
    },
    "servers": [
        {"url": "/", "description": "Servidor Atual / Local"}
    ],
    "tags": [
        {"name": "Clientes", "description": "Gerenciamento de clientes da barbearia"},
        {"name": "Barbeiros", "description": "Gerenciamento de profissionais barbeiros"}
    ],
    "paths": {
        "/clientes": {
            "get": {
                "tags": ["Clientes"],
                "summary": "Listar clientes",
                "description": "Retorna uma lista paginada de clientes com suporte a filtros parciais por nome e email.",
                "parameters": [
                    {
                        "name": "nome",
                        "in": "query",
                        "description": "Filtro parcial por nome",
                        "required": False,
                        "schema": {"type": "string", "example": "joao"}
                    },
                    {
                        "name": "email",
                        "in": "query",
                        "description": "Filtro parcial por email",
                        "required": False,
                        "schema": {"type": "string", "example": "example.com"}
                    },
                    {
                        "name": "page",
                        "in": "query",
                        "description": "Número da página (padrão: 1)",
                        "required": False,
                        "schema": {"type": "integer", "default": 1}
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "Itens por página (padrão: 10, máx: 100)",
                        "required": False,
                        "schema": {"type": "integer", "default": 10}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Lista de clientes recuperada com sucesso",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ClientePaginacao"}
                            }
                        }
                    },
                    "400": {
                        "description": "Parâmetros de paginação inválidos",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErroGenerico"}
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Clientes"],
                "summary": "Criar cliente",
                "description": "Cadastra um novo cliente na barbearia.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ClienteInput"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Cliente criado com sucesso",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Cliente"}
                            }
                        }
                    },
                    "400": {
                        "description": "Corpo da requisição ausente ou JSON inválido",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErroGenerico"}
                            }
                        }
                    },
                    "422": {
                        "description": "Erro de validação no payload",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErroValidacao"}
                            }
                        }
                    }
                }
            }
        },
        "/clientes/{id}": {
            "get": {
                "tags": ["Clientes"],
                "summary": "Detalhar cliente",
                "description": "Recupera os detalhes de um cliente específico pelo ID.",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "ID numérico do cliente",
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Dados do cliente",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Cliente"}
                            }
                        }
                    },
                    "404": {
                        "description": "Cliente não encontrado",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErroGenerico"}
                            }
                        }
                    }
                }
            },
            "put": {
                "tags": ["Clientes"],
                "summary": "Substituir cliente (PUT)",
                "description": "Atualização completa dos dados de um cliente existente.",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "ID numérico do cliente",
                        "schema": {"type": "integer"}
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ClienteInput"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Cliente atualizado com sucesso",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Cliente"}
                            }
                        }
                    },
                    "400": {"description": "JSON inválido", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}},
                    "404": {"description": "Cliente não encontrado", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}},
                    "422": {"description": "Erro de validação", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroValidacao"}}}}
                }
            },
            "patch": {
                "tags": ["Clientes"],
                "summary": "Atualizar parcialmente cliente (PATCH)",
                "description": "Atualiza campos específicos de um cliente.",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "ID numérico do cliente",
                        "schema": {"type": "integer"}
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ClientePatchInput"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Cliente atualizado com sucesso",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Cliente"}
                            }
                        }
                    },
                    "400": {"description": "Nenhum campo fornecido ou JSON inválido", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}},
                    "404": {"description": "Cliente não encontrado", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}},
                    "422": {"description": "Erro de validação", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroValidacao"}}}}
                }
            },
            "delete": {
                "tags": ["Clientes"],
                "summary": "Remover cliente",
                "description": "Exclui um cliente da base de dados.",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "ID numérico do cliente",
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "204": {"description": "Cliente removido com sucesso (sem corpo de resposta)"},
                    "404": {"description": "Cliente não encontrado", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}}
                }
            }
        },
        "/barbeiros": {
            "get": {
                "tags": ["Barbeiros"],
                "summary": "Listar barbeiros",
                "description": "Retorna uma lista paginada de profissionais barbeiros com filtros por nome e status ativo.",
                "parameters": [
                    {
                        "name": "nome",
                        "in": "query",
                        "description": "Filtro parcial por nome",
                        "required": False,
                        "schema": {"type": "string", "example": "carlos"}
                    },
                    {
                        "name": "ativo",
                        "in": "query",
                        "description": "Filtro por status (true/false)",
                        "required": False,
                        "schema": {"type": "boolean", "example": True}
                    },
                    {
                        "name": "page",
                        "in": "query",
                        "description": "Número da página",
                        "required": False,
                        "schema": {"type": "integer", "default": 1}
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "Itens por página",
                        "required": False,
                        "schema": {"type": "integer", "default": 10}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Lista de barbeiros recuperada com sucesso",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/BarbeiroPaginacao"}
                            }
                        }
                    },
                    "400": {
                        "description": "Parâmetro 'ativo' ou de paginação inválido",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErroGenerico"}
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Barbeiros"],
                "summary": "Criar barbeiro",
                "description": "Cadastra um novo barbeiro.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/BarbeiroInput"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Barbeiro cadastrado com sucesso",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Barbeiro"}
                            }
                        }
                    },
                    "400": {"description": "JSON inválido", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}},
                    "422": {"description": "Erro de validação no payload", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroValidacao"}}}}
                }
            }
        },
        "/barbeiros/{id}": {
            "get": {
                "tags": ["Barbeiros"],
                "summary": "Detalhar barbeiro",
                "description": "Recupera os detalhes de um barbeiro pelo ID.",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "ID numérico do barbeiro",
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Dados do barbeiro",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Barbeiro"}
                            }
                        }
                    },
                    "404": {"description": "Barbeiro não encontrado", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}}
                }
            },
            "put": {
                "tags": ["Barbeiros"],
                "summary": "Substituir barbeiro (PUT)",
                "description": "Atualização integral dos dados do barbeiro.",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "ID do barbeiro",
                        "schema": {"type": "integer"}
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/BarbeiroInput"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Barbeiro atualizado com sucesso",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Barbeiro"}
                            }
                        }
                    },
                    "400": {"description": "JSON inválido", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}},
                    "404": {"description": "Barbeiro não encontrado", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}},
                    "422": {"description": "Erro de validação", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroValidacao"}}}}
                }
            },
            "patch": {
                "tags": ["Barbeiros"],
                "summary": "Atualizar parcialmente barbeiro (PATCH)",
                "description": "Atualiza campos específicos de um barbeiro.",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "ID do barbeiro",
                        "schema": {"type": "integer"}
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/BarbeiroPatchInput"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Barbeiro atualizado com sucesso",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Barbeiro"}
                            }
                        }
                    },
                    "400": {"description": "Nenhum campo fornecido ou JSON inválido", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}},
                    "404": {"description": "Barbeiro não encontrado", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}},
                    "422": {"description": "Erro de validação", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroValidacao"}}}}
                }
            },
            "delete": {
                "tags": ["Barbeiros"],
                "summary": "Remover barbeiro",
                "description": "Exclui um barbeiro da base de dados.",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "ID do barbeiro",
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "204": {"description": "Barbeiro removido com sucesso (sem corpo)"},
                    "404": {"description": "Barbeiro não encontrado", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroGenerico"}}}}
                }
            }
        }
    },
    "components": {
        "schemas": {
            "ClienteInput": {
                "type": "object",
                "required": ["nome", "telefone"],
                "properties": {
                    "nome": {"type": "string", "minLength": 2, "maxLength": 120, "example": "João da Silva"},
                    "telefone": {"type": "string", "minLength": 8, "maxLength": 20, "example": "11999998888"},
                    "email": {"type": "string", "format": "email", "example": "joao@example.com"}
                }
            },
            "ClientePatchInput": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "minLength": 2, "maxLength": 120, "example": "João Silva"},
                    "telefone": {"type": "string", "minLength": 8, "maxLength": 20, "example": "11900000000"},
                    "email": {"type": "string", "format": "email", "example": "novo.email@example.com"}
                }
            },
            "Cliente": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "nome": {"type": "string", "example": "João da Silva"},
                    "telefone": {"type": "string", "example": "11999998888"},
                    "email": {"type": "string", "example": "joao@example.com"},
                    "data_cadastro": {"type": "string", "format": "date-time", "example": "2026-08-31T20:00:00"}
                }
            },
            "ClientePaginacao": {
                "type": "object",
                "properties": {
                    "dados": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Cliente"}
                    },
                    "paginacao": {
                        "type": "object",
                        "properties": {
                            "pagina": {"type": "integer", "example": 1},
                            "por_pagina": {"type": "integer", "example": 10},
                            "total": {"type": "integer", "example": 1},
                            "total_paginas": {"type": "integer", "example": 1}
                        }
                    }
                }
            },
            "BarbeiroInput": {
                "type": "object",
                "required": ["nome"],
                "properties": {
                    "nome": {"type": "string", "minLength": 2, "maxLength": 120, "example": "Carlos Machado"},
                    "especialidade": {"type": "string", "maxLength": 100, "example": "Degradê e Barboterapia"},
                    "telefone": {"type": "string", "minLength": 8, "maxLength": 20, "example": "11977776666"},
                    "ativo": {"type": "boolean", "default": True, "example": True}
                }
            },
            "BarbeiroPatchInput": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "minLength": 2, "maxLength": 120, "example": "Carlos Machado Silva"},
                    "especialidade": {"type": "string", "maxLength": 100, "example": "Corte Clássico"},
                    "telefone": {"type": "string", "minLength": 8, "maxLength": 20, "example": "11988887777"},
                    "ativo": {"type": "boolean", "example": False}
                }
            },
            "Barbeiro": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "nome": {"type": "string", "example": "Carlos Machado"},
                    "especialidade": {"type": "string", "example": "Degradê e Barboterapia"},
                    "telefone": {"type": "string", "example": "11977776666"},
                    "ativo": {"type": "boolean", "example": True}
                }
            },
            "BarbeiroPaginacao": {
                "type": "object",
                "properties": {
                    "dados": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/Barbeiro"}
                    },
                    "paginacao": {
                        "type": "object",
                        "properties": {
                            "pagina": {"type": "integer", "example": 1},
                            "por_pagina": {"type": "integer", "example": 10},
                            "total": {"type": "integer", "example": 1},
                            "total_paginas": {"type": "integer", "example": 1}
                        }
                    }
                }
            },
            "ErroGenerico": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Mensagem descritiva do erro"}
                }
            },
            "ErroValidacao": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Erro de validacao no payload"},
                    "detalhes": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "example": {"nome": ["Length must be between 2 and 120."]}
                    }
                }
            }
        }
    }
}
