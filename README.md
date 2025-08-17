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











# p1_talera --------------------------------------------------

=> Para activar el entorno virtual.
    COMANDO:
      source .venv/Scripts/activate
      deactivate

    COMANDO PARA INSTALAR DEPENDENCIAS DE DESARROLLO:
      pip install ruff black mypy pytest uvicorn httpie

  Para Compilar:
    uvicorn app.main:app --reload

    
Consola A → Docker
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

