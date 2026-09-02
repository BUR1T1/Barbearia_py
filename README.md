# API RESTful - Barbearia (Flask)

API RESTful para gestao de uma **barbearia**, feita em Python/Flask com persistencia
relacional, ORM, controle de versao de schema e arquitetura em camadas.

Trabalho da disciplina *Desenvolvimento de API RESTful com Flask* (2a Avaliacao A2).

---

## 1. Dominio e modelagem

Dominio: **barbearia**. Modelo completo implementado:

| Entidade        | Descricao                                          | Responsavel      |
|-----------------|---------------------------------------------------|------------------|
| **Cliente**     | Pessoas atendidas pela barbearia                  | Otavio (feito)   |
| **Barbeiro**    | Profissionais que executam os servicos            | Membro 2 (feito) |
| **Servico**     | Catalogo de servicos (corte, barba, etc.)         | Membro 3 (feito) |
| **Agendamento** | Horario marcado; liga Cliente, Barbeiro e Servico | Membro 4 (feito) |

### Relacionamentos

```
Cliente  1 ----- N  Agendamento  N ----- 1  Barbeiro
                         |
                         | N ----- N
                         |
                      Servico   (tabela associativa agendamento_servicos)
```

- `Cliente 1:N Agendamento` - um cliente tem varios agendamentos.
- `Barbeiro 1:N Agendamento` - um barbeiro atende varios agendamentos.
- `Agendamento N:N Servico` - um agendamento pode ter varios servicos.

As chaves estrangeiras (`ForeignKey`) e a integridade referencial ficam na
entidade **Agendamento**.

---

## 2. Arquitetura em camadas

```
Requisicao HTTP
   |
   v
Rotas (app/routes/)      -> interpreta a requisicao, define o status code
   |
   v
Esquemas (app/schemas/)  -> valida e serializa o payload (erro -> 422)
   |
   v
Servicos (app/services/) -> regras de negocio, usa o ORM
   |
   v
Models (app/models/)     -> mapeamento objeto-relacional
   |
   v
Banco de dados (SQLite)
```

- As rotas nunca acessam o banco direto: sempre chamam a camada de servico.
- Os erros sao tratados de forma central em `app/errors/`, devolvendo sempre
  JSON no formato `{"error": "mensagem"}`.
- A configuracao vem de variaveis de ambiente (`.env`), nunca fixa no codigo.

### Tecnologias

| Item        | Tecnologia                        |
|-------------|-----------------------------------|
| Framework   | Flask 3                           |
| ORM         | Flask-SQLAlchemy                  |
| Migrations  | Flask-Migrate                     |
| Validacao   | Marshmallow                       |
| Testes      | pytest                            |
| Banco       | SQLite (padrao) / MySQL (opcional) |
| Config      | python-dotenv                     |

---

## 3. Estrutura de pastas

```
Barbearia_py/
├── app/
│   ├── __init__.py            # criar_app(): registra blueprints e tratadores de erro
│   ├── extensions.py          # instancias db e migrate
│   ├── errors/
│   │   ├── exceptions.py      # ErroAPI, NaoEncontrado
│   │   └── handlers.py        # registrar_tratadores_de_erro()
│   ├── models/                # cliente.py, barbeiro.py, servico.py, agendamento.py
│   ├── schemas/               # *_schema.py (validacao/serializacao)
│   ├── services/              # *_service.py (regras de negocio)
│   └── routes/                # *_routes.py (endpoints REST)
├── migrations/                # versionamento de schema (Flask-Migrate/Alembic)
│   └── versions/              # 654ad4148b15_estrutura_inicial.py
├── tests/                     # testes pytest
│   ├── conftest.py            # fixtures (client, dados_base)
│   ├── test_clientes.py
│   ├── test_barbeiros.py
│   ├── test_servicos.py
│   └── test_agendamentos.py
├── instance/                  # banco SQLite gerado (barbearia.db)
├── config.py                  # classe Configuracao (le o .env)
├── run.py                     # ponto de entrada
├── pytest.ini                 # configuracao do pytest (pythonpath)
├── requests.http              # testes HTTP
├── requirements.txt
├── .env.example
└── README.md
```

---

## 4. Como rodar

Pre-requisito: Python 3.11+

```bash
# 1. Ambiente virtual
python -m venv venv
source venv/bin/activate            # Linux/Mac
# .venv\Scripts\Activate.ps1        # Windows (PowerShell)

# 2. Dependencias
pip install -r requirements.txt

# 3. Variaveis de ambiente
cp .env.example .env                # Linux/Mac (copy no Windows)

# 4. Criar o schema via migrations versionadas
flask --app run.py db upgrade
#   Alternativa rapida sem migrations: flask --app run.py criar-banco

# 5. Subir a API
flask --app run.py run
# http://localhost:5000
```

Teste rapido: `curl http://localhost:5000/clientes` ou abra `requests.http` no VS Code.
Documentacao interativa: `http://localhost:5000/docs` (Swagger UI).

---

## 5. Endpoints

Todas as entidades seguem o mesmo padrao REST. Base de cada uma:
`/clientes`, `/barbeiros`, `/servicos`, `/agendamentos`.

| Metodo | Rota              | Descricao                       | Sucesso |
|--------|-------------------|---------------------------------|---------|
| GET    | `/<recurso>`      | Lista com filtros e paginacao   | 200     |
| GET    | `/<recurso>/<id>` | Detalha um registro             | 200     |
| POST   | `/<recurso>`      | Cria um registro                | 201     |
| PUT    | `/<recurso>/<id>` | Atualizacao completa            | 200     |
| PATCH  | `/<recurso>/<id>` | Atualizacao parcial             | 200     |
| DELETE | `/<recurso>/<id>` | Remove um registro              | 204     |

### Filtros por entidade

| Entidade      | Filtros disponiveis                          |
|---------------|----------------------------------------------|
| Cliente       | `nome`, `email`                              |
| Barbeiro      | `nome`, `ativo`                              |
| Servico       | `nome`, `preco_min`, `preco_max`             |
| Agendamento   | `cliente_id`, `barbeiro_id`, `status`        |

Paginacao (todas): `page` (default 1) e `per_page` (default 10, max 100).

Resposta da listagem:

```json
{
  "dados": [
    { "id": 1, "nome": "Joao da Silva", "telefone": "11999998888",
      "email": "joao@example.com", "data_cadastro": "2026-08-29T23:30:59" }
  ],
  "paginacao": { "pagina": 1, "por_pagina": 10, "total": 1, "total_paginas": 1 }
}
```

### Exemplos

```bash
# Criar cliente (201)
curl -X POST http://localhost:5000/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome":"Joao da Silva","telefone":"11999998888","email":"joao@example.com"}'

# Criar agendamento ligando cliente + barbeiro + servicos (201)
curl -X POST http://localhost:5000/agendamentos \
  -H "Content-Type: application/json" \
  -d '{"data_hora":"2026-09-03T14:30:00","cliente_id":1,"barbeiro_id":1,"servico_ids":[1]}'

# Remover (204)
curl -X DELETE http://localhost:5000/clientes/1
```

---

## 6. Status codes e tratamento de erros

| Codigo | Quando                                                    |
|--------|----------------------------------------------------------|
| 200    | GET / PUT / PATCH com sucesso                            |
| 201    | POST com sucesso                                         |
| 204    | DELETE com sucesso (sem corpo)                           |
| 400    | Corpo ausente ou JSON invalido                           |
| 404    | Recurso ou identificador inexistente                     |
| 422    | Erro de validacao/tipagem no payload                     |
| 500    | Erro interno nao previsto                                |

Formato das respostas de erro:

```json
{ "error": "Mensagem descritiva" }
```

Erros de validacao incluem `detalhes`:

```json
{
  "error": "Erro de validacao no payload",
  "detalhes": { "telefone": ["Missing data for required field."] }
}
```

---

## 7. Migrations (Flask-Migrate)

O schema e versionado com Flask-Migrate (Alembic). A pasta `migrations/` ja esta
no repositorio, com a versao inicial em
`migrations/versions/654ad4148b15_estrutura_inicial.py`.

```bash
# Aplicar as migrations e criar o schema (uso normal)
flask --app run.py db upgrade

# Gerar uma nova migration apos alterar os models
flask --app run.py db migrate -m "descricao da mudanca"
flask --app run.py db upgrade
```

> `flask db init` so e necessario uma vez, ao criar o projeto. Como a pasta
> `migrations/` ja existe, rodar `db init` de novo retorna erro (esperado) -
> use direto o `db upgrade`.

---

## 8. Testes (pytest)

Os testes cobrem o CRUD feliz de cada entidade e os casos de erro 404 e 422,
alem do fluxo de relacionamentos do agendamento (cliente + barbeiro + servicos).

A raiz do projeto tem um `pytest.ini` que adiciona o diretorio ao `PYTHONPATH`,
para que `from app import criar_app` funcione ao rodar `pytest` de qualquer
terminal, sem precisar exportar variavel manualmente:

```ini
[pytest]
pythonpath = .
testpaths = tests
```

Rodar a suite:

```bash
pytest
```

Saida esperada:

```
tests/test_agendamentos.py ..
tests/test_barbeiros.py .....
tests/test_clientes.py .....
tests/test_servicos.py .....

17 passed
```

Os testes usam um banco SQLite temporario por execucao (fixture `client` em
`tests/conftest.py`), sem tocar no `instance/barbearia.db` de desenvolvimento.

---

## 9. Divisao de tarefas

### Feito - Otavio
- Estrutura do projeto e fabrica da aplicacao (`criar_app`), config via `.env`.
- Integracao de Flask-SQLAlchemy e Flask-Migrate (`app/extensions.py`).
- Camada de erros global (`app/errors/`): `ErroAPI` / `NaoEncontrado` +
  `registrar_tratadores_de_erro`, cobrindo 400 / 404 / 422 / 500.
- Entidade **Cliente** completa (model + schema + service + routes), servindo de
  modelo de referencia, com paginacao e filtros.
- Comando `flask criar-banco`, base do `requests.http` e do README.

### Feito - Membro 2: entidade **Barbeiro**
- CRUD completo (6 verbos), paginacao e filtros por `nome` e `ativo`.
- 404 para id inexistente, 422 para payload invalido.

### Feito - Membro 3: entidade **Servico**
- CRUD completo, validacao de `preco` positivo e `duracao_min` positivo.
- Filtros `nome`, `preco_min`, `preco_max`; 422 quando `preco` <= 0.

### Feito - Membro 4: entidade **Agendamento** + relacionamentos
- Model com FKs para Cliente e Barbeiro e N:N com Servico via
  `agendamento_servicos`.
- Validacao de existencia de cliente, barbeiro e servicos antes de criar/atualizar
  (422 quando referencia nao existe).
- `GET /agendamentos/<id>` retorna os dados relacionados aninhados.

### Feito - Membro 5: Flask-Migrate + testes + documentacao
- Migrations versionadas em `migrations/` (`db upgrade` cria todo o schema).
- Suite `pytest` com CRUD feliz de cada entidade + casos 404 e 422
  (**17 testes passando**), `pytest` no `requirements.txt` e `pytest.ini` para
  resolver o `PYTHONPATH`.
- `requests.http` completo cobrindo todos os endpoints e status codes
  (200 / 201 / 204 / 400 / 404 / 422).
- README atualizado com as instrucoes de migrations e testes.

---

## 10. Defesa de codigo - pontos para dominar

- Fluxo `requisicao -> rota -> esquema -> servico -> model -> banco`.
- Como o Marshmallow gera o `422` e onde ele e capturado (`app/errors/handlers.py`).
- Diferenca entre `PUT` (payload completo) e `PATCH` (`partial=True`, campos opcionais).
- Como as `ForeignKey` e o relacionamento N:N sao declarados no `Agendamento`.
- Por que a configuracao vem do `.env` e nao do codigo.
- Por que existe o `pytest.ini`: sem ele, `pytest` nao encontra o pacote `app`
  (a raiz do projeto nao entra no `sys.path` automaticamente).
- Diferenca entre `db upgrade` (aplica migrations versionadas) e `criar-banco`
  (cria as tabelas direto, sem versionamento).