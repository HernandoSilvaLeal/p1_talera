# 🚀 Order Processing Service (FastAPI + MongoDB)

## 📌 Purpose
This repository contains a **minimal, production-minded Order Processing Service** built with **FastAPI** and **MongoDB**.  
It demonstrates:  
- Hands-on engineering quality (**clean code, domain boundaries, testing, observability**).  
- Architectural thinking (**serverless/event-driven fit for AWS**).  

---

## 🤝 Why this fits the customer company
The customer company operates a **web-based platform** that runs **compute-intensive operations via APIs** and requires **multi-tenant, scalable backend services**.  

Although this kata uses “orders”, the **same architectural patterns** apply to real-world workloads such as:  
- Design & simulation requests  
- Report generation  

Key reusable concepts: **idempotency, clear state transitions, async processing, logging, error handling**.  

---

## 📊 Evaluation Alignment

### ✅ Clarity & Professionalism
- Consistent project structure  
- One-command startup (**Docker Compose**)  
- Clear, developer-friendly README  

### ✅ Code Quality
- Strongly typed **Pydantic models**  
- **Automated tests**  
- Lint / format / type checks with:  
  - [ruff](https://github.com/astral-sh/ruff)  
  - [black](https://github.com/psf/black)  
  - [mypy](http://mypy-lang.org/)  

### ✅ Architecture & Communication
- Concise **1-pager** describing serverless + event-driven AWS deployment  
- Clear, **non-technical language** for stakeholders  

### ✅ Relevance & Feasibility
- Pragmatic trade-offs  
- Extensible to **multi-service deployments**  

### ✅ Time Management
- Opinionated tooling to **speed up onboarding & code reviews**  

---

# 🔎 Rapid & Comprehensive Project Review

This section lets you verify the project’s **technical, functional, and quality** status quickly.  
The idea is to work with **dedicated terminals**, separating responsibilities as in a professional environment.

---

## 🧭 Working Model with Dedicated Terminals

- **Terminal 1 – Boot & Status**  
- **Terminal 2 – Observability (logs & health)**  
- **Terminal 3 – Tests (unit/integration)**  
- **Terminal 4 – Code Quality (linters & typing)**  
- **Terminal 5 – Database (MongoDB inspection)**  
- **Terminal 6 – Dependencies (Poetry)**

> Tip: keep each terminal open in its own tab/window.

---

## 🖥️ Terminal 1 – Boot & Status

Start the services and check their state.

~~~bash
docker compose up --build
docker compose ps
~~~

---

## 📊 Terminal 2 – Observability

Tail logs and validate the service health.

~~~bash
docker compose logs -f app
docker compose logs -f mongo
curl http://127.0.0.1:8000/health
~~~

---

## ✅ Terminal 3 – Tests

Run unit and integration tests.

~~~bash
pytest -v
pytest tests/test_health.py
~~~

---

## 🧹 Terminal 4 – Code Quality

Check formatting, static errors, and typing.

~~~bash
black .
ruff check .
mypy .
~~~

---

## 📂 Terminal 5 – Database

Open MongoDB shell to inspect data and collections.

~~~bash
docker exec -it p1-mongo-1 mongosh   # replace with your actual container name if different
show dbs
use <your_db_name>
db.orders.findOne()
db.orders.getIndexes()
~~~

---

## 📦 Terminal 6 – Dependencies (Poetry)

Manage libraries and lockfiles.

~~~bash
poetry install
poetry add <package>
poetry update
poetry export -f requirements.txt --output requirements.txt --without-hashes
~~~

---

## ✅ Quick Review Checklist

- [ ] Project starts cleanly with `docker compose up`.
- [ ] Endpoints work in Swagger and `/health` returns healthy status.
- [ ] Logs are visible and readable from the observability terminal.
- [ ] Unit and integration tests pass.
- [ ] Linters and typing checks report no critical issues.
- [ ] MongoDB is accessible and collections are present.
- [ ] Dependencies are in sync via Poetry.

---

## 🎯 Expected Outcome

With these 6 terminals and the checklist you ensure:

- 🚀 The project runs without errors.  
- 📦 Dependencies remain consistent.  
- 📊 Logs and health signals are under control.  
- ✅ Tests and linters are executed.  
- 🗄️ The database is reachable and validated.

---











# p1_talera --------------------------------------------------

=> Para activar el entorno virtual.
    COMANDO:
      source .venv/Scripts/activate
      deactivate

    COMANDO PARA INSTALAR DEPENDENCIAS DE DESARROLLO:
      pip install ruff black mypy pytest uvicorn httpie

  Para Compilar:
    uvicorn app.main:app --reload

# comands --------------------------------------------------

Levantar limpio
    docker compose down
    docker compose up -d --build
    docker compose ps

docker info

Ver logs de arranque
    docker logs p1-app-1 --tail=50

Probar liveness y readiness
    curl -i http://localhost:8000/healthz
    curl -i http://localhost:8000/ready

Probar logs por request
    curl -i http://localhost:8000/healthz
    docker logs p1-app-1 --tail=50

Para correr los test
    poetry run pytest





🖥️ Consola 1 – Ejecución del Proyecto (infraestructura viva)
  # Levantar el proyecto con Docker Compose
      docker compose up --build

  # Levantar en background (modo demonio)
      docker compose up -d

  # Apagar servicios
      docker compose down

  # Ver estado de contenedores
      docker compose ps

  # Ver logs en tiempo real de la app
      docker compose logs -f app


🖥️ Consola 2 – Observabilidad y Monitoreo
  # Logs en vivo de Mongo
      docker compose logs -f mongo

  # Logs en vivo de la app
      docker compose logs -f app

  # Healthcheck manual vía curl
      curl http://127.0.0.1:8000/health

  # Swagger UI (abrir en navegador)
      http://127.0.0.1:8000/docs


🖥️ Consola 3 – Tests y Validación Rápida
  # Correr todos los tests
    poetry run pytest

  # Tests con cobertura
    poetry run pytest --cov=app

  # Test específico (ej: health)
    poetry run pytest tests/test_health.py -v


🖥️ Consola 4 – Estilo, Linter y Calidad de Código
  # Linter ruff (rápido y estricto)
    poetry run ruff check app

  # Formateo automático con black
    poetry run black app

  # Revisión de typing
    poetry run mypy app


🖥️ Consola 5 – Base de Datos y Debug
# Abrir shell de Mongo dentro del contenedor
docker exec -it mongo mongosh

# Ver bases de datos
show dbs

# Usar la DB específica
use mydb

# Ver colecciones
show collections

# Revisar índices
db.orders.getIndexes()


🖥️ Consola 6 – Gestión de dependencias y entorno
  # Instalar dependencias del proyecto
    poetry install

  # Agregar una nueva dependencia
    poetry add <paquete>

  # Agregar solo para desarrollo (ej: pytest, black, mypy)
    poetry add --group dev <paquete>

  # Actualizar dependencias
    poetry update















    
Consola A → Docker
    docker compose up --build  # Cuando queiro ejecutar la version mas reciente de docker, dependencias y codigo.
    
    docker-compose up -d       # levantar servicios
    docker-compose down        # apagarlos
    docker ps                  # ver qué está corriendo
    docker logs -f p1-app-1    # ver logs de la app
    docker logs -f p1-mongo-1  # ver logs de Mongo

Consola B → Cliente de la aplicación (tests)
    curl http://127.0.0.1:8000/health
    curl -X POST http://127.0.0.1:8000/orders ...

Consola C → Desarrollo (local) (opcional)
    Solo la usas si quieres levantar FastAPI sin Docker (modo desarrollo).
    uvicorn app.main:app --reload
    ⚠️ Ojo: si usas Docker no necesitas esta consola, salvo que quieras probar rápido la app sin contenedores.

Consola D → Mongo Shell / Tools (opcional)
    Solo si quieres entrar a MongoDB para inspeccionar datos manualmente.
    docker exec -it p1-mongo-1 mongosh

    con consultas como:
      use orders
      db.orders.find()














***************************
Opcionales:
Perfecto, Nando. Te preparo la forma más práctica de que tu entorno .venv se active automáticamente cada vez que abras VS Code en tu proyecto, sin que tengas que escribir source .venv/Scripts/activate manualmente.

















[CTX v1-mini]
Goal: FastAPI+Mongo Order Service; endpoints: POST(idempotent via Idempotency-Key), GET/{id}, PATCH/{id} with If-Match version & state machine (CREATED→{PAID,CANCELLED}; PAID→{FULFILLED,CANCELLED}).
Stack: Py3.11, FastAPI, Pydantic v2, Motor, pytest/httpx, ruff/black/mypy, Docker, .env.
Money: Decimal→JSON string. Idempotency: unique key + TTL.
Reply FORMAT: one file per turn → give path + exact file content only, overwrite, no explanations. If cross-file change needed → propose minimal diff first.

AHORA QUE TE DI CONTEXTO TE ENVIO LA TAREA EXACTA QUE DEBES RESOLVER
Patch `app/main.py` to REMOVE any `@app.on_event("startup")` block that calls ensure_indexes.
Keep only the `lifespan` asynccontextmanager already defined. Do not change anything else. No explanations.

DETENTE EN CUANTO LA RESUELVAS TAL CUAL Y ME CONFIRMAS ASL RESPECTO CON LO QUE HICISTE














***
PRIMERO AQUI VA EL CONTEXTO GENERAL DE QUE ESTAMOS HACIENDO A NIVEL GLOBAL 
    ROLE: Senior backend+solution architect, pair-programming agent. Do NOT mention real company; say “customer company”.
    GOAL: Build a minimal, production-minded Order Processing Service.
    STACK: Python 3.11, FastAPI, Pydantic v2, Motor (MongoDB), pytest(+asyncio), httpx, ruff, black, mypy, Docker+Compose, .env.
    LAYOUT (fixed):
    app/{main.py,config.py,domain/{models.py,entities.py,errors.py},infra/{mongo.py,logging.py},routes/orders.py,services/orders_service.py,utils/{idempotency.py,request_context.py}}
    tests/, docs/{ARCHITECTURE.md, ADR-0001-tech-choices.md}, requirements.txt, pyproject.toml, .env.example, Dockerfile, docker-compose.yml, .editorconfig, .gitignore, README.md

    API CONTRACT (strict):
    - POST /orders: uses OrderIn; computes amount; idempotent via header "Idempotency-Key" (store marker w/ TTL); returns 201 + Location + OrderOut.
    - GET /orders/{id}: 200 with OrderOut or 404.
    - PATCH /orders/{id}: body {status}; validate transitions:
      CREATED→{PAID,CANCELLED}; PAID→{FULFILLED,CANCELLED}; FULFILLED→{}; CANCELLED→{}.
      Concurrency: header "If-Match" = version (int). On mismatch → 409.

    DOMAIN:
    - Money as Decimal (no float). OrderOut serializes Decimal as string.
    - Keep rules in domain; service orchestrates; infra handles Mongo.

    NON-FUNCTIONAL:
    - JSON logging + X-Request-Id middleware.
    - Centralized HTTP errors (400/404/409/422 shape).
    - Idempotency: unique index on key + TTL index on expires_at.
    - OpenAPI clean; tests cover idempotency, transitions, optimistic locking.

    WORKFLOW (one file per turn):
    - Reply ONLY with the single file requested: 1) path, 2) full content. No explanations.
    - Overwrite file if exists. No extra files unless I ask.
    - If another file must change, propose the minimal diff first.
    - Keep code/comments/docs in English.

***
SEGUNDO, YA QUE TIENES EL CONTEXTO GENERAL, AHORA AYUDAME A RESOLVER LOS ERRORES QUE TENGO EN CONSOLA SOBRE: 
    $ ruff check . --fix && black . && mypy .

***
TERCERO PARA QUE ME AYUDES A RESOVLER ESTOS ERRORES, AQUI VA EL DETALLE DE MIS INSTRUCCIONES:
    Actúa como un revisor senior de código Python en un proyecto con FastAPI y MongoDB. 
    Te paso los hallazgos de linting y calidad (Ruff/Black/Mypy) y necesito que:
    1. Corrijas el código fuente en los archivos indicados (main.py, routes/orders.py, tests/*).
    2. Apliques buenas prácticas sugeridas:
      - No usar `try/except/pass` sin loggear (S110).
      - En bloques `except`, usar `raise ... from e` para mantener el contexto (B904).
      - Revisar el uso de `assert` en tests: decide si reemplazar por helpers de pytest o documentar la decisión de mantenerlos.
    3. Actualices mi `pyproject.toml` para usar las nuevas claves `lint.ignore` y `lint.select`.
    4. Opcional: configura Ruff para ignorar la regla `S101` SOLO en la carpeta `tests/`.
    5. Entregues un **informe final** con:
      - Lista de cambios aplicados por archivo.
      - Justificación arquitectónica/pedagógica de cada cambio.
      - Código corregido listo para pegar.

    Hallazgos iniciales Ruff/Black/Mypy:
    - `S110` en app/main.py (try/except/pass).
    - `B904` en app/routes/orders.py (raise sin from).
    - `S101` en tests/test_domain_state_machine.py y tests/test_orders_api.py (uso de assert).
    - Aviso de Ruff: mover opciones de `ignore` y `select` a `lint.ignore` y `lint.select` en pyproject.toml.

    Entrega todo como si fueras el revisor final de un Pull Request: 
    primero el informe resumido de cambios, luego los diffs o snippets de código corregidos.

*** 
CON LO ANTERIOR, EL RESULTADO EXITOSO ES QUE YO EJECUTE:
   ruff check . --fix && black . && mypy .
   en mi console de gitbash y me de como resultado, calidad de codigo sin errores.

***
SI EL RESULTADO ES EXITOSO, DAME UN INFORME CONCISO DE EXITO, PARA COMUNICAR FLUJO DE TRABAJO.

