# API RESTful - Barbearia (Flask)

API RESTful para gestao de uma **barbearia**, feita em Python/Flask com persistencia
relacional, ORM, controle de versao de schema e arquitetura em camadas.

Trabalho da disciplina *Desenvolvimento de API RESTful com Flask* (2a Avaliacao A2).

---

## 1. Dominio e modelagem

Dominio: **barbearia**. Modelo completo previsto:

| Entidade        | Descricao                                          | Responsavel      |
|-----------------|---------------------------------------------------|------------------|
| **Cliente**     | Pessoas atendidas pela barbearia                  | Otavio (feito)   |
| **Barbeiro**    | Profissionais que executam os servicos            | Membro 2 (TODO)  |
| **Servico**     | Catalogo de servicos (corte, barba, etc.)         | Membro 3 (TODO)  |
| **Agendamento** | Horario marcado; liga Cliente, Barbeiro e Servico | Membro 4 (TODO)  |

### Relacionamentos previstos

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
entidade **Agendamento** (TODO do Membro 4).

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
| Migrations  | Flask-Migrate                    |
| Validacao   | Marshmallow                      |
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
│   ├── models/
│   │   └── cliente.py         # entidade Cliente
│   ├── schemas/
│   │   └── cliente_schema.py  # EsquemaCliente (validacao/serializacao)
│   ├── services/
│   │   └── cliente_service.py # regras de negocio de Cliente
│   └── routes/
│       └── cliente_routes.py  # endpoints REST de Cliente
├── config.py                  # classe Configuracao (le o .env)
├── run.py                     # ponto de entrada
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
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows (PowerShell)
# source .venv/bin/activate         # Linux/Mac

# 2. Dependencias
pip install -r requirements.txt

# 3. Variaveis de ambiente
copy .env.example .env             # Windows  (cp no Linux/Mac)

# 4. Criar as tabelas
flask --app run.py criar-banco
#   (quando as migrations estiverem prontas - TODO Membro 5 - usar: flask --app run.py db upgrade)

# 5. Subir a API
flask --app run.py run
# http://localhost:5000
```

Teste rapido: `curl http://localhost:5000/clientes` ou abra `requests.http` no VS Code.

---

## 5. Endpoints implementados (Cliente)

Base: `/clientes`

| Metodo | Rota             | Descricao                       | Sucesso |
|--------|------------------|---------------------------------|---------|
| GET    | `/clientes`      | Lista com filtros e paginacao   | 200     |
| GET    | `/clientes/<id>` | Detalha um cliente              | 200     |
| POST   | `/clientes`      | Cria um cliente                 | 201     |
| PUT    | `/clientes/<id>` | Atualizacao completa            | 200     |
| PATCH  | `/clientes/<id>` | Atualizacao parcial             | 200     |
| DELETE | `/clientes/<id>` | Remove um cliente               | 204     |

### Filtros e paginacao (GET `/clientes`)

| Parametro  | Exemplo              | Efeito                              |
|------------|----------------------|-------------------------------------|
| `nome`     | `?nome=joao`         | Busca parcial por nome              |
| `email`    | `?email=example.com` | Busca parcial por email             |
| `page`     | `?page=2`            | Pagina (default 1)                  |
| `per_page` | `?per_page=20`       | Itens por pagina (default 10, max 100) |

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
# Criar (201)
curl -X POST http://localhost:5000/clientes \
  -H "Content-Type: application/json" \
  -d '{"nome":"Joao da Silva","telefone":"11999998888","email":"joao@example.com"}'

# Atualizacao parcial (200)
curl -X PATCH http://localhost:5000/clientes/1 \
  -H "Content-Type: application/json" -d '{"telefone":"11900000000"}'

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

## 7. Divisao de tarefas

### Feito - Otavio

- Estrutura do projeto e fabrica da aplicacao (`criar_app`), configuracao via
  `.env` (`config.py`).
- Integracao de Flask-SQLAlchemy e Flask-Migrate (`app/extensions.py`).
- Camada de erros global (`app/errors/`): `ErroAPI` / `NaoEncontrado` +
  `registrar_tratadores_de_erro`, cobrindo 400 / 404 / 422 / 500.
- Entidade **Cliente** completa, servindo de **modelo de referencia**:
  `model` + `schema` + `service` + `routes` (Blueprint).
- CRUD completo de Cliente (GET lista, GET id, POST, PUT, PATCH, DELETE) com
  status codes semanticos, **paginacao** e **filtros** (`nome`, `email`).
- Comando `flask criar-banco`, arquivo `requests.http` e este README.

> Padrao a seguir: cada nova entidade replica os 4 arquivos de Cliente
> (`models/X.py`, `schemas/X_schema.py`, `services/X_service.py`,
> `routes/X_routes.py`), registra o blueprint em `app/__init__.py` e importa o
> model em `app/models/__init__.py`.

---

### TODO - Membro 2: entidade **Barbeiro** (CRUD completo)

Seguir o padrao de Cliente:

- **Model** `app/models/barbeiro.py` - campos: `id`, `nome` (obrigatorio),
  `especialidade` (str), `telefone` (str), `ativo` (bool, default `True`).
- **Esquema** `app/schemas/barbeiro_schema.py` com validacoes de tamanho/tipo.
- **Servico** `app/services/barbeiro_service.py` - CRUD + paginacao + filtro por
  `nome` e por `ativo`.
- **Rotas** `app/routes/barbeiro_routes.py` - blueprint `/barbeiros` com os 6
  verbos (GET lista, GET id, POST 201, PUT 200, PATCH 200, DELETE 204).
- Registrar o blueprint em `app/__init__.py` e importar o model em
  `app/models/__init__.py`. Adicionar os testes de `/barbeiros` no `requests.http`.

**Pronto quando:** os 6 verbos funcionam, 404 para id inexistente, 422 para
payload invalido.

---

### TODO - Membro 3: entidade **Servico** (CRUD completo)

Seguir o padrao de Cliente:

- **Model** `app/models/servico.py` - campos: `id`, `nome` (obrigatorio),
  `descricao` (str), `preco` (`db.Numeric(10, 2)`, obrigatorio, > 0),
  `duracao_min` (int, > 0).
- **Esquema** `app/schemas/servico_schema.py` - validar `preco` positivo
  (`validate.Range(min=0.01)`) e `duracao_min` positivo.
- **Servico** `app/services/servico_service.py` - CRUD + paginacao + filtros
  `nome`, `preco_min`, `preco_max`.
- **Rotas** `app/routes/servico_routes.py` - blueprint `/servicos` com os 6 verbos.
- Registrar blueprint + importar model. Adicionar testes de `/servicos` no
  `requests.http`.

**Pronto quando:** CRUD completo, 422 quando `preco` <= 0, filtro de faixa de
preco funcionando.

---

### TODO - Membro 4: entidade **Agendamento** + relacionamentos

Esta entidade amarra o modelo relacional (FK + integridade referencial).

- **Model** `app/models/agendamento.py`:
  - `id`, `data_hora` (datetime, obrigatorio), `status` (str: `agendado` /
    `concluido` / `cancelado`, default `agendado`), `observacao` (str, opcional).
  - `cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)`
  - `barbeiro_id = db.Column(db.Integer, db.ForeignKey("barbeiros.id"), nullable=False)`
  - N:N com `Servico` via tabela associativa `agendamento_servicos`.
  - `relationship` para `cliente`, `barbeiro` e `servicos`.
- Adicionar o lado inverso em `Cliente` e `Barbeiro` (ha um comentario pronto
  indicando o local em `app/models/cliente.py`).
- **Esquema** `app/schemas/agendamento_schema.py` - validar `cliente_id`,
  `barbeiro_id` e a lista `servico_ids`.
- **Servico** `app/services/agendamento_service.py` - CRUD + paginacao + filtros
  (`cliente_id`, `barbeiro_id`, `status`). Antes de criar/atualizar, **conferir
  que cliente, barbeiro e servicos existem**; se nao, `422` (usar `ErroAPI` com
  status 422). Retornar o agendamento com os dados relacionados aninhados.
- **Rotas** `app/routes/agendamento_routes.py` - blueprint `/agendamentos`, 6 verbos.
- Registrar blueprint + importar model. Adicionar testes de `/agendamentos` no
  `requests.http`.

**Pronto quando:** da para criar um agendamento ligando 1 cliente, 1 barbeiro e
1+ servicos; `GET /agendamentos/<id>` mostra os dados relacionados.

---

### TODO - Membro 5: Flask-Migrate + testes + documentacao

- Inicializar as **migrations**: `flask --app run.py db init`, depois
  `db migrate -m "estrutura inicial"` e `db upgrade`. Versionar a pasta
  `migrations/` no repositorio.
- Completar o `requests.http` (ou entregar colecao Postman/Insomnia) cobrindo
  todos os endpoints e todos os status codes (200/201/204/400/404/422).
- Escrever testes com **pytest** em `tests/` (CRUD feliz de cada entidade + casos
  404 e 422). Adicionar `pytest` ao `requirements.txt`.
- Opcional: script de `seed` para popular o banco.
- Atualizar este README com as instrucoes finais de migrations e testes.

**Pronto quando:** `flask db upgrade` cria todo o schema, `pytest` passa e a
colecao HTTP cobre todos os endpoints.

---

## 8. Defesa de codigo - pontos para dominar

- Fluxo `requisicao -> rota -> esquema -> servico -> model -> banco`.
- Como o Marshmallow gera o `422` e onde ele e capturado (`app/errors/handlers.py`).
- Diferenca entre `PUT` (payload completo) e `PATCH` (`partial=True`, campos opcionais).
- Como as `ForeignKey` e o relacionamento N:N sao declarados no `Agendamento`.
- Por que a configuracao vem do `.env` e nao do codigo.
