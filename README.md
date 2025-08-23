# 🚀 Order Processing Service — FastAPI + MongoDB (Serverless-Ready)

A **minimal yet production-minded Order Processing Service** built with **FastAPI**, **MongoDB (async with Motor)**, and **Docker/Poetry**.  
It demonstrates **real-world backend patterns**: idempotent `POST` requests, optimistic locking with `If-Match`, explicit state machine transitions, structured logging, observability, and extensibility toward **serverless/event-driven AWS architectures**.  

> 📐 Architectural diagrams are **included and socialized**: C4 Context, Container, Sequence diagrams (POST & PATCH flows), and AWS reference architecture.

---

## 📚 Table of Contents
- [📦 Stack & Architecture](#-stack--architecture)
- [⚡ TL;DR (Quick Start)](#-tldr-quick-start)
- [🚀 Local Execution (Development)](#-local-execution-development)
- [🐳 Docker & Compose](#-docker--compose)
- [✅ Tests & Quality](#-tests--quality)
- [🔍 Observability](#-observability)
- [🗄️ Database](#-database)
- [⚙️ Configuration (ENV)](#️-configuration-env)
- [🧩 API Reference (Summary)](#-api-reference-summary)
- [🔐 Design Decisions (Summary)](#-design-decisions-summary)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [☁️ AWS Production One-Pager](#️-aws-production-one-pager)
- [🛡️ Security & Compliance (PCI-DSS/GDPR)](#️-security--compliance-pci-dssgdpr)
- [📐 Architectural Diagrams (Socialization)](#-architectural-diagrams-socialization)
- [🗺️ Roadmap (0–6 Months)](#️-roadmap-06-months)
- [✅ Definition of Done & Quality Gates](#-definition-of-done--quality-gates)
- [📄 License / Authors / Links](#-license--authors--links)


# 📦 Stack & Architecture

### 🛠️ Technologies
- **Language & Framework**: Python 3.11, FastAPI, Pydantic v2  
- **Database**: MongoDB (asynchronous access with Motor)  
- **Tooling**: Poetry (dependency & venv management), Pytest (testing), Ruff (linter), Black (formatter), Mypy (type checker)  
- **Containerization**: Docker + Docker Compose  
- **Observability**: Structured JSON logging, Prometheus-ready metrics, health endpoints  

---

### 🧩 Services & Ports
| Service       | Description                       | Host:Container |
|---------------|-----------------------------------|----------------|
| `app`         | FastAPI application (Uvicorn)     | 8000:8000      |
| `mongo`       | MongoDB database                  | 27017:27017    |
| `test-runner` | Ephemeral container for test runs | N/A            |

---

### 📐 High-Level Diagram (Textual)

## 🔗 High-Level Flow (Textual Diagram)

```text
[Client/CLI/cURL]
        │
        ▼
   HTTP (REST)
        │
        ▼
 [API FastAPI] ──→ [Infra / Logging JSON + Metrics]
        │
        │  async I/O (Motor)
        ▼
     [MongoDB]
        ├─ orders (main collection)
        └─ idempotency_keys (TTL + unique index)
```









# ⚡ TL;DR (fast start)

**Minimum** commands to run, test, and check health. Copy/paste according to your environment.

**Local (hot-reload)**
```bash
# (opcional) preparar variables
cp .env.example .env

# ejecutar API en desarrollo
uvicorn app.main:app --reload
```

**Tests rápidos**
```bash
pytest -q
```

**Docker (build + up)**
```bash
docker compose up -d --build
docker compose ps
docker compose logs -f app
```

**Healthcheck (expects 200 OK)**
```bash
curl -s http://127.0.0.1:8000/health
# -> {"status":"ok","mongo":"ok"}
```

**Swagger / OpenAPI**
```text
http://127.0.0.1:8000/docs
```

**Shutdown and clean up**
```bash
docker compose down -v
```
















## 🧭 Architecture Diagrams

> High-level view first, then focused views per concern. Each diagram includes a short legend (1–2 lines) to anchor the reader.

![Architecture — Global Overview with 12 subdiagrams](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578080/DiagramTotalResume_12Subs_oo9s3x.png)

### Index
- [1) Containers & Context](#1-containers--context)  
- [2) Components — Clean Architecture](#2-components--clean-architecture)  
- [3) Request E2E — POST /orders (Idempotency)](#3-request-e2e--post-orders-idempotency)  
- [4) State Machine & Versions](#4-state-machine--versions)  
- [5) Idempotency Flow](#5-idempotency-flow)  
- [6) Health & Observability](#6-health--observability)  
- [7) Database & Indexes](#7-database--indexes)  
- [8) Concurrency — Optimistic Locking](#8-concurrency--optimistic-locking)  
- [9) Error Matrix — HTTP](#9-error-matrix--http)  
- [10) API Surface & Contracts](#10-api-surface--contracts)  
- [11) Testing Pyramid](#11-testing-pyramid)  
- [12) Local Deployment (dev/prod)](#12-local-deployment-devprod)

---

## 📂 Repositorio de Diagramas de Arquitectura

Este apartado contiene el enlace al repositorio central en Google Drive donde se encuentran todos los diagramas de arquitectura, recursos y documentación visual relacionados con la prueba técnica.

### Enlace de Acceso

> **[Acceder a la carpeta de Google Drive con todos los diagramas](https://drive.google.com/drive/folders/1YrU69ewttq6xY9WrZ94qkP-xwTQ_UWGO?usp=sharing)**

### Estructura del Contenido

La carpeta principal está organizada en tres subdirectorios clave para facilitar la consulta:

* **`1. AWS Architecture aws_talera`**
    * En esta carpeta se encuentran las distintas versiones y la versión final del diagrama de arquitectura diseñado para ser desplegado en AWS.
    * Incluye carpetas como:
        * `AWS_Diagram_version1`
        * `AWS_Diagram_version2`
        * `AWS_Diagram_version3`
        * `AWS_Diagram_version4_Final`
        * `AWS_CloudFormation_Code_Deploy_Cloud`

* **`2. Diagrams Architecture (12)`**
    * Contiene una colección curada de los 12 diagramas más relevantes que explican a fondo componentes y flujos específicos de la solución.
    * Aborda temas como:
        * Máquinas de estado (Generales y específicas).
        * Flujo de Idempotencia.
        * Salud y Observabilidad del sistema.
        * Estrategias de Base de Datos e Índices.
        * Manejo de Concurrencia y Bloqueo Optimista.
        * Pirámide de Testing.

* **`3. FILES Diagrams Full`**
    * Este directorio alberga la colección completa y más detallada de todos los diagramas generados.
    * Es el lugar ideal para buscar un diagrama específico o ver la visión de conjunto.
    * Incluye diagramas de resumen general (`DiagramTotalResume_C1Dev.png`, `DiagramTotalResume_C4Devs.png`) y otros sobre:
        * Contenedores y Contexto (C1).
        * Componentes y Arquitectura Limpia (C2).
        * Flujos E2E para peticiones POST.
        * Despliegue local.


---

### 1 Containers & Context

![Diagram 1 — Containers and Context](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578091/DiagramArchitecture1_Containers_and_Context_v5j7d3.png)

**Legend (EN):** Context boundaries across client/API/infra. Requests traverse HTTP → FastAPI → Mongo, with structured logging and correlation IDs.

---

### 2 Components — Clean Architecture

![Diagram 2 — Clean Architecture Components](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578092/DiagramArch2_Components_Clean_Ar___Mermaid_Chart-2025-08-18-202419_vesond.png)

**Legend (EN):** Layered separation (routes/services/domain/infra). DTOs validated at the edge; domain rules enforced centrally; infra is swappable.

---

### 3 Request E2E — POST /orders (Idempotency)

![Diagram 3 — E2E POST orders with Idempotency](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578089/DiagramArch3_Request_E2E_POST_orders_Ide___Mermaid_Chart-2025-08-18-212312_lpk1nj.png)

**Legend (EN):** End-to-end flow for order creation using `Idempotency-Key`. Guarantees exactly-once effect under retries and network glitches.

---

### 4 State Machine & Versions

![Diagram 4 — State Machine (small)](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578088/DiagramArch4_Small_StateMachine_Flow_yi2gf7.png)

![Diagram 4 — State Machine (big)](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578089/DiagramArch4_Big_StateMachine_i5ueev.png)

**Legend (EN):** Explicit state transitions with optimistic versioning. PATCH enforces legal transitions and rejects invalid paths with domain errors.

---

### 5 Idempotency Flow

![Diagram 5 — Idempotency Flow](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578084/DiagramArch5_Idempotency_Flow_xplv7x.png)

**Legend (EN):** Storage-backed key registry (TTL + unique index). Replays return the original response; diverging payloads yield conflict.

---

### 6 Health & Observability

![Diagram 6 — Health and Observability](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578087/DiagramArch6_Health_and_Observability_hoopxn.png)

**Legend (EN):** Probes for liveness/deps (Mongo ping). Structured JSON logs, request IDs, and metrics surfaces for SRE dashboards.

---

### 7 Database & Indexes

![Diagram 7 — Database and Indexes](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578085/DiagramArch7_Database_and_Indexes_jjdyde.png)

**Legend (EN):** Collections: `orders`, `idempotency_keys`. Critical indexes: unique business keys and TTL to cap storage for replay windows.

---

### 8 Concurrency — Optimistic Locking

![Diagram 8 — Optimistic Locking](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578088/DiagramArch8_Concurrency_Optimistic_Lock_fqdobc.png)

**Legend (EN):** Version field + `If-Match/ETag` contract prevent lost updates. Conflicting writers receive `409 Conflict`.

---

### 9 Error Matrix — HTTP

![Diagram 9 — HTTP Error Matrix](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578080/DiagramArch9_Error_Matrix_HTTP_nhdopt.png)

**Legend (EN):** Canonical error shapes mapped to HTTP: 400 validation, 404 not found, 409 conflict, 422 domain violations, 5xx infra failures.

---

### 10 API Surface & Contracts

![Diagram 10 — API Surface and Contracts](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578081/DiagramArch10_API_Surface_Contracts_t3swwx.png)

**Legend (EN):** Public endpoints and headers of interest. Emphasizes idempotent POST and PATCH preconditions using ETag semantics.

---

### 11 Testing Pyramid

![Diagram 11 — Testing Pyramid](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578080/DiagramArch11_Testing_Pyramid_sfpj8s.png)

**Legend (EN):** Heavier focus on unit/domain tests; selective integration/e2e coverage for critical flows (idempotency, state transitions).

---

### 12 Local Deployment (dev/prod)

![Diagram 12 — Local Deployment dev/prod](https://res.cloudinary.com/dqvny6ewr/image/upload/v1755578076/DiagramArch12_Local_Deployment_dev_prod_jni95h.png)

**Legend (EN):** Docker Compose for local dev parity; environment contracts mirror production (Mongo, app, test runner).





























# 🚀 Local Execution (Development)

Run the application locally in development mode with hot-reload and Poetry-managed virtual environment.

**Prerequisites**
- Python 3.11+
- [Poetry](https://python-poetry.org/) ≥ 1.7
- MongoDB running locally or via Docker
- Docker Desktop (optional but recommended)

---

**1️⃣ Setup Environment**
```bash
# Clean old environments (optional)
poetry env list
poetry env remove --all

# Install dependencies (including dev)
poetry install --with dev --no-interaction --no-ansi

# Copy environment variables
cp .env.example .env
```

---

**2️⃣ Run the Application**
```bash
poetry run uvicorn app.main:app --reload
```

By default, the API will be available at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- Healthcheck: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

**3️⃣ Hot Reload for Developers**
- Any code changes are reloaded automatically.  
- Logs are displayed in the console with JSON structure.  

---

**4️⃣ Example Validation**
```bash
curl -s http://127.0.0.1:8000/health
# -> {"status":"ok","mongo":"ok"}
```













# 🐳 Docker & Compose

Run the entire stack with Docker Compose for a reproducible, containerized environment.

---

**1️⃣ Build & Start Services**
```bash
docker compose up -d --build
```

**2️⃣ Check Running Containers**
```bash
docker compose ps
```

**3️⃣ View Logs in Real Time**
```bash
docker compose logs -f app
docker compose logs -f mongo
```

**4️⃣ Healthcheck**
```bash
curl -s http://127.0.0.1:8000/health
# -> {"status":"ok","mongo":"ok"}
```

**5️⃣ Swagger UI**
Open in your browser:
```text
http://127.0.0.1:8000/docs
```

**6️⃣ Stop & Clean Up**
```bash
docker compose down -v
```

---

### Notes
- `app` service: FastAPI + Uvicorn (port **8000:8000**)  
- `mongo` service: MongoDB (port **27017:27017**)  
- Network & volume management handled automatically by Docker Compose.  
- For a clean state, always use `docker compose down -v` to remove volumes.  










# ✅ Tests & Quality

Ensure code correctness and maintain high quality with automated tests, linters, and type checks.

---

**1️⃣ Run All Tests**
```bash
pytest -q -vv
```

**2️⃣ Run Specific Test (example: health)**
```bash
pytest tests/test_health.py -v
```

**3️⃣ Coverage Report (optional)**
```bash
pytest --cov=app
```

---

**4️⃣ Code Quality Checks**
- **Linting (Ruff)**  
- **Formatting (Black)**  
- **Static Typing (Mypy)**

```bash
ruff check . --fix
black .
mypy .
```

---

**5️⃣ Reproducible Tests via Docker**
Run tests inside an ephemeral container to guarantee a clean environment:
```bash
docker compose run --rm test-runner pytest -q -vv
```

---

### Quality Gates
- ✅ All tests must pass  
- ✅ `ruff`, `black`, `mypy` with **zero critical issues**  
- ✅ Coverage target ≥ 70` (recommended)  








# 🔍 Observability

Visibility into system health, logs, and metrics is critical for operating this service in production-like environments.

---

**1️⃣ Health Endpoint**
- **URL**: `/health`  
- **200 OK** → `{"status":"ok","mongo":"ok"}`  
- **503 Service Unavailable** → `{"status":"degraded","mongo":"fail"}`  

```bash
curl -s http://127.0.0.1:8000/health
```

---

**2️⃣ Structured Logging (JSON)**
Every request and domain event is logged with contextual fields:
- `ts` — timestamp  
- `level` — INFO, ERROR, etc.  
- `request_id` — correlation id per request  
- `order_id` — business identifier (if available)  
- `action` — operation (create_order, update_order, etc.)  
- `status` — outcome or order state  
- `latency_ms` — request duration  
- `error_code` — present if failure occurred  

**Sample log entry**
```json
{
  "ts": "2025-08-18T12:00:00Z",
  "level": "INFO",
  "request_id": "f6f1a2...",
  "action": "create_order",
  "order_id": "664d3f...",
  "status": "CREATED",
  "latency_ms": 18
}
```

---

**3️⃣ Metrics (Prometheus-ready)**
Exported counters and histograms:  
- `http_requests_total{path,method,status}`  
- `order_state_transitions_total{from,to}`  
- `idempotency_hits_total{hit|miss}`  
- `mongo_ops_latency_ms` (histogram)  

Future integration with **Prometheus + Grafana** for dashboards and alerts.

---

**4️⃣ Logs & Monitoring via Docker**
```bash
docker compose logs -f app
docker compose logs -f mongo
```

Use multiple terminals for dedicated monitoring streams (recommended during dev/test).  











# 🗄️ Database

This service relies on **MongoDB** as its persistence layer, optimized for asynchronous operations and scalability.

---

### 📂 Main Collections

**1️⃣ `orders`**
- Fields:
  - `_id` (ObjectId)
  - `order_id` (UUID/string)
  - `version` (int → optimistic locking)
  - `status` (enum: `CREATED | PAID | FULFILLED | CANCELLED`)
  - `items[] { sku, qty, price (Decimal as string) }`
  - `currency` (e.g., `USD`)
  - `amount_total` (calculated, Decimal as string)
- Indexes:
  - `{ order_id: 1 }` → optional unique index for faster lookups

**2️⃣ `idempotency_keys`**
- Fields:
  - `key` (string, unique)
  - `response` (cached API response body)
  - `created_at`
  - `expires_at` (Date)
- Indexes:
  - `key` → **unique index**
  - `expires_at` → **TTL index** (automatic cleanup)

---

### 🔑 Index Management

Example commands inside Mongo shell:

```bash
# Access Mongo shell
docker exec -it mongo mongosh

# Use target database
use orders_db

# Create unique index for idempotency keys
db.idempotency_keys.createIndex({ key: 1 }, { unique: true })

# Create TTL index (e.g., expire after 24h)
db.idempotency_keys.createIndex({ expires_at: 1 }, { expireAfterSeconds: 0 })

# Verify indexes
db.orders.getIndexes()
```

---

### 📊 Data Seeding / Debugging

For quick tests you can insert a mock order:

```bash
db.orders.insertOne({
  order_id: "demo-123",
  version: 1,
  status: "CREATED",
  currency: "USD",
  items: [{ sku: "SKU-1", qty: 2, price: "19.99" }],
  amount_total: "39.98"
})
```







# ⚙️ Configuration (ENV)

The service is configured through environment variables. Copy the sample file and adjust as needed:

```bash
cp .env.example .env
```

---

### 📑 Environment Variables

| Variable             | Description                                 | Example                                   |
|----------------------|---------------------------------------------|-------------------------------------------|
| `APP_ENV`            | Execution environment                       | `local` \| `dev` \| `prod`                |
| `APP_HOST`           | Host interface for FastAPI                  | `0.0.0.0`                                 |
| `APP_PORT`           | Port for FastAPI                            | `8000`                                    |
| `MONGO_URI`          | Connection string for MongoDB               | `mongodb://mongo:27017`                   |
| `MONGO_DB`           | Database name                               | `orders_db`                               |
| `LOG_LEVEL`          | Logging level                               | `INFO`                                    |
| `IDEMPOTENCY_TTL_S`  | TTL (seconds) for idempotency keys          | `86400`                                   |
| `CORS_ORIGINS`       | Comma-separated list of allowed origins     | `http://localhost:3000,http://127.0.0.1`  |

---

Complete/adjust according to your deployment. Keep secrets out of the repo (use a secret manager in the cloud).

### 🔒 Notes
- Keep `.env` **out of source control**.  
- In production, prefer a **secrets manager** (AWS Secrets Manager, Vault, etc.).  
- Adjust `CORS_ORIGINS` carefully for security (default should be restrictive).  
- The TTL for idempotency keys (`IDEMPOTENCY_TTL_S`) should align with expected retry policies of your clients.  











# 🧩 API Reference (Summary)

This service exposes a **REST API** for managing orders with strong guarantees of **idempotency**, **optimistic locking**, and **explicit state transitions**.

---

### 📌 Endpoints

| Method | Path               | Description                                  | Notes |
|--------|--------------------|----------------------------------------------|-------|
| `POST` | `/orders`          | Create a new order                           | Idempotent via `Idempotency-Key` header |
| `GET`  | `/orders/{orderId}`| Retrieve an order by ID                      | Returns `200` or `404` |
| `PATCH`| `/orders/{orderId}`| Update order status                          | Requires `If-Match` header for version |
| `GET`  | `/health`          | Service health check (app + DB)              | Returns `200` or `503` |

---

### 🔄 State Machine

CREATED → { PAID, CANCELLED }
PAID → { FULFILLED, CANCELLED }
FULFILLED → { } CANCELLED → { }


Invalid transitions will return **422 Unprocessable Entity**.

---

### 📥 Request & Response Examples

**Create Order (idempotent)**  
Headers must include `Idempotency-Key`.

```bash
curl -s -X POST http://127.0.0.1:8000/orders \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: key-001" \
  -d '{
    "customer_id":"c-1",
    "currency":"USD",
    "items":[{"sku":"A1","qty":2,"price":"9.99"}]
  }'
```

_Response (201 Created)_
```json
{
  "order_id": "o-123",
  "version": 1,
  "status": "CREATED",
  "currency": "USD",
  "amount_total": "19.98",
  "items": [
    { "sku": "A1", "qty": 2, "price": "9.99" }
  ]
}
```

---

**Update Order (optimistic lock)**  
Headers must include the last known `If-Match` version.

```bash
curl -s -X PATCH http://127.0.0.1:8000/orders/o-123 \
  -H "If-Match: 1" \
  -H "Content-Type: application/json" \
  -d '{"status":"PAID"}'
```

_Response (200 OK)_
```json
{
  "order_id": "o-123",
  "version": 2,
  "status": "PAID",
  "currency": "USD",
  "amount_total": "19.98"
}
```

_Response (409 Conflict on wrong version)_
```json
{
  "type": "https://example.com/problems/conflict",
  "title": "Version conflict",
  "status": 409,
  "detail": "If-Match does not match current resource version",
  "trace_id": "abc123"
}
```

---

### ⚠️ Error Model (Unified)

All error responses follow a **Problem Details**-like schema:

```json
{
  "type": "https://example.com/problems/invalid-state",
  "title": "Invalid transition",
  "status": 422,
  "detail": "Cannot transition from FULFILLED to PAID",
  "trace_id": "xyz789"
}
```















# 🔐 Design Decisions (Summary)

The system is intentionally built to demonstrate **production-grade backend patterns** that ensure reliability, scalability, and clarity.

---

### 1️⃣ Idempotency
- Implemented in `POST /orders` via the `Idempotency-Key` header.  
- Each key is stored in the `idempotency_keys` collection with:
  - **Unique index** (prevents duplicates)
  - **TTL index** (automatic expiration after configured period)  
- Guarantees: **same key → same response** (safe retries for clients).

---

### 2️⃣ Optimistic Locking
- Implemented in `PATCH /orders/{id}` using the `If-Match` header.  
- Each order stores a `version` integer, incremented on updates.  
- If `If-Match` does not match current `version` → **409 Conflict** returned.  
- Prevents lost updates in concurrent scenarios.

---

### 3️⃣ Explicit State Machine
- Domain logic enforces valid state transitions:
  - `CREATED → {PAID, CANCELLED}`
  - `PAID → {FULFILLED, CANCELLED}`
  - Terminal states (`FULFILLED`, `CANCELLED`) cannot transition further.  
- Invalid transitions return **422 Unprocessable Entity**.

---

### 4️⃣ Money as Decimal
- Monetary values handled with `Decimal` (not float).  
- Serialized as **string** in API responses.  
- Ensures accuracy and avoids floating-point rounding issues.

---

### 5️⃣ Clean Layered Architecture
- **Routes** → define API contracts (FastAPI routers).  
- **Services** → orchestrate use cases (idempotency, validation, persistence).  
- **Domain** → models, entities, and business rules.  
- **Infra** → MongoDB driver, logging, metrics.  
- **Utils** → helpers (idempotency key, request context).

---

### 6️⃣ Observability & Error Handling
- **Structured logs (JSON)** with request correlation (`request_id`).  
- **Metrics** exposed for Prometheus (HTTP requests, state transitions, DB ops latency).  
- **Centralized error model**: consistent Problem Details JSON (`400`, `404`, `409`, `422`, `503`).  
- Health endpoint (`/health`) checks Mongo availability.

---

### 7️⃣ Extensibility
- Local-first with Docker Compose and Poetry.  
- Designed to **scale to Kubernetes** or **migrate to AWS serverless**:
  - API Gateway + Lambda (FastAPI with Mangum)
  - DynamoDB (idempotency TTL)
  - DocumentDB (orders persistence)
  - EventBridge + Step Functions (event-driven workflows)
- CI/CD ready (GitHub Actions, CodePipeline, or similar).  












# 🛠️ Troubleshooting

Common issues and quick fixes when running or developing this service.

---

### 1️⃣ Port Conflicts
- **Symptom**: `Address already in use` when starting FastAPI.  
- **Fix**: Change `APP_PORT` in `.env`, or free the port.  
```bash
# On Linux/Mac
lsof -i :8000
kill -9 <PID>

# On Windows
netstat -ano | find "8000"
taskkill /PID <PID> /F
```

---

### 2️⃣ MongoDB Not Available
- **Symptom**: `/health` endpoint returns `503` with `"mongo":"fail"`.  
- **Fix**: Check container logs and ensure Mongo is running.  
```bash
docker compose logs -f mongo
```

---

### 3️⃣ Idempotency Issues
- **Symptom**: `POST /orders` does not return the same response on retry.  
- **Fix**: Verify:
  - The same `Idempotency-Key` header is used.  
  - The TTL index exists in `idempotency_keys`.  
```bash
db.idempotency_keys.getIndexes()
```

---

### 4️⃣ Version Conflicts on PATCH
- **Symptom**: `PATCH /orders/{id}` returns `409 Conflict`.  
- **Fix**: Fetch the latest order (`GET /orders/{id}`) and retry with the correct `version` in `If-Match`.

---

### 5️⃣ Docker Volumes / Clean State
- **Symptom**: Stale data or schema errors.  
- **Fix**: Remove volumes and restart fresh.  
```bash
docker compose down -v
docker compose up -d --build
```

---

### 6️⃣ Dependency Sync Issues
- **Symptom**: Missing package errors.  
- **Fix**: Reinstall Poetry environment.  
```bash
poetry env remove --all
poetry install --with dev
```














# ☁️ AWS Production One-Pager

This service is designed to seamlessly extend into a **serverless, event-driven architecture** on AWS, ensuring scalability, resilience, and cost efficiency.

---

### 🔄 Flow Overview
1. **API Gateway** → Entry point for client requests.  
2. **Lambda (FastAPI via Mangum)** → Executes application logic.  
3. **Persistence**:  
   - **DocumentDB (Mongo-compatible)** → Orders and state machine.  
   - **DynamoDB (TTL)** → Idempotency keys with automatic expiration.  
4. **EventBridge** → Publishes domain events (`OrderCreated`, `OrderUpdated`).  
5. **Step Functions** → Orchestrates multi-step business processes.  
6. **SQS + DLQ** → Ensures reliability with dead-letter queues.  
7. **Kinesis Firehose → S3 (Parquet)** → Audit/event storage, queryable with Athena/Glue.  

---

### 🔐 Security
- **IAM least privilege** for every component.  
- **KMS** for encryption at rest (keys for DocumentDB, DynamoDB, S3).  
- **Secrets Manager** for database credentials and API keys.  
- **WAF** to block malicious traffic at the edge.  
- **VPC isolation** for sensitive workloads.  

---

### 📊 Observability
- **CloudWatch Logs & Metrics** for monitoring application and infra.  
- **X-Ray tracing** for distributed requests.  
- Structured JSON logs remain consistent with local dev.  

---

### ⚙️ CI/CD
- **Pipeline**: CodePipeline (or GitHub Actions) → CodeBuild → CodeDeploy (canary release).  
- **Infrastructure as Code**: AWS CDK or Terraform for reproducible environments.  
- **Testing Stages**: Unit, Integration, Canary, Rollback safety nets.  

---

### ⚖️ Trade-Offs
- **Lambda vs ECS**: Lambda is cost-efficient for bursty workloads; ECS better for long-lived processes.  
- **DocumentDB vs Atlas**: DocumentDB = AWS-native, but Atlas offers more Mongo features.  
- **DynamoDB TTL vs Redis**: DynamoDB TTL is managed and simpler; Redis offers microsecond latency.  

---

### 🌐 Why This Design
- **Scalable** to millions of daily transactions.  
- **Cost-per-use** via Lambda reduces idle expenses.  
- **Event-driven** for decoupled services.  
- **Auditable** with complete event history stored in S3.  













# 🛡️ Security & Compliance (PCI-DSS/GDPR)

Operating in financial or multi-tenant contexts requires strict attention to **security** and **regulatory compliance**.  
This section summarizes best practices aligned with **PCI-DSS** (payments) and **GDPR** (data protection).

---

### 🔒 Data Protection
- **Encryption in transit**: Enforce TLS 1.2+ on all endpoints.  
- **Encryption at rest**: Use AWS KMS / CMK for DocumentDB, DynamoDB, S3.  
- **Secrets Management**: Store sensitive values in AWS Secrets Manager or HashiCorp Vault. Never commit secrets to source control.  

---

### 📑 PCI-DSS Considerations
- **Cardholder Data**: Do not store raw PAN (Primary Account Number). Use tokenization providers.  
- **Access Control**: IAM roles follow **least privilege principle**; multi-factor authentication for operators.  
- **Logging & Monitoring**: Immutable logs (S3 + Object Lock) for traceability.  
- **Regular Penetration Testing**: Validate compliance and security posture.  

---

### 🌍 GDPR Considerations
- **Right to Erasure ("Right to be Forgotten")**: Orders and related data can be deleted or anonymized when required.  
- **Data Retention Policies**: Apply TTL on collections (e.g., idempotency keys) and define retention per domain.  
- **Consent & Purpose Limitation**: Only collect customer data necessary for order processing.  
- **Data Residency**: Ensure hosting in compliant regions (EU if required).  

---

### 🛡️ Network & Perimeter Security
- **WAF**: Protect against injection, XSS, and common OWASP Top 10 attacks.  
- **Rate Limiting & Throttling**: Mitigate abuse and DoS attacks.  
- **VPC Isolation**: Place sensitive services in private subnets with no public access.  

---

### 📊 Compliance Monitoring
- **CloudTrail**: Governance and audit logging across AWS accounts.  
- **GuardDuty / Security Hub**: Threat detection and compliance dashboards.  
- **CI/CD Security Gates**: Static analysis, dependency scanning, secrets detection before deployment.  

---

> ✅ By combining these controls, the system aligns with **PCI-DSS Level 1** requirements and supports **GDPR compliance** for personal data processing.  











# 📐 Architectural Diagrams (Socialization)

To ensure both technical and business stakeholders clearly understand the system, this project **includes and socializes architectural diagrams** stored in `docs/DIAGRAMS/`.  

These diagrams are embedded in documentation (README, slides) and presented during design reviews.  

---

### 🗺️ C4 Model

1. **Context Diagram (C4-1)**  
   - Shows actors (clients, developers, monitoring systems).  
   - Defines boundaries: Order Processing Service vs external systems (e.g., payment providers, messaging bus).  

2. **Container Diagram (C4-2)**  
   - Highlights FastAPI service, MongoDB, Observability stack.  
   - Includes Docker Compose services (`app`, `mongo`, `test-runner`).  

3. **Component Diagram (C4-3)**  
   - Details layers: Routes, Services, Domain, Infra, Utils.  
   - Shows dependencies (Pydantic, Motor, Logging, Metrics).  

---

### 🔄 Sequence Diagrams

- **POST /orders**  
  Flow with `Idempotency-Key`:  
  Client → API → Idempotency collection (hit/miss) → Orders collection → Response.  

- **PATCH /orders**  
  Flow with `If-Match`:  
  Client → API → Orders (check `version`) → Update or `409 Conflict`.  

---

### ☁️ AWS Reference Architecture

Diagram illustrates the **serverless/event-driven production setup**:  
API Gateway → Lambda (FastAPI via Mangum) → DocumentDB/DynamoDB → EventBridge → Step Functions → SQS (DLQ) → Kinesis Firehose → S3 (Parquet, queryable via Athena).  

Includes observability layers (CloudWatch, X-Ray), and security controls (IAM, KMS, WAF, Secrets Manager, VPC).  

---

### 📊 Diagram Socialization

- All diagrams are exported as **PNG/SVG** and versioned in `docs/DIAGRAMS/`.  
- Embedded thumbnails in README; high-resolution in docs and slides.  
- Used in stakeholder sessions to bridge **technical depth** and **business clarity**.  













# 🗺️ Roadmap (0–6 Months)

A high-level roadmap that balances **technical milestones** with **business value delivery**, ensuring the service evolves from MVP to production-grade at scale.

---

### 📍 Month 0–1: MVP Delivery
- Core REST API operational:
  - `POST /orders` with idempotency
  - `GET /orders/{id}`
  - `PATCH /orders/{id}` with optimistic locking
- Healthcheck endpoint + structured logging
- Docker Compose for reproducible local environment
- CI/CD pipeline skeleton (tests + lint + type checks)
- Initial architectural diagrams (C4 Context, Container, Sequences)

---

### 📍 Month 2–3: Hardening & Observability
- Add Prometheus metrics (requests, transitions, idempotency hit/miss)
- Dashboard integration (Grafana or equivalent)
- Define alerting rules (latency, error rate, Mongo connectivity)
- Improve security:
  - Strict CORS configuration
  - Input validation and payload limits
- Integration tests with in-memory Mongo (mongomock or test containers)

---

### 📍 Month 3–4: Serverless Proof of Concept
- Deploy FastAPI with Mangum on AWS Lambda
- Replace local Mongo with AWS DocumentDB
- DynamoDB for idempotency keys with TTL
- EventBridge publishing `OrderCreated/Updated` events
- Step Functions orchestration demo (e.g., payment + fulfillment flow)

---

### 📍 Month 4–5: Compliance & Multi-Tenancy
- Draft **COMPLIANCE.md** with PCI-DSS/GDPR mappings
- Add data retention policies with TTL on collections
- Multi-tenant support: namespace per tenant or partitioned keys
- Security review: IAM roles, secrets handling, WAF policies

---

### 📍 Month 5–6: Production Readiness
- Full CI/CD pipeline with:
  - Unit + integration tests
  - Static analysis (Ruff, Mypy, Bandit)
  - Deployment stages (dev → staging → prod)
  - Canary releases & rollback strategy
- Operational runbooks for on-call engineers
- Chaos testing for resilience validation
- Cost and latency optimization (Lambda cold starts, indexes, query patterns)

---

### 🚀 Beyond 6 Months (Stretch Goals)
- Advanced analytics: Firehose → S3 (Parquet) → Athena/Glue queries
- Machine learning integration for fraud detection or demand forecasting
- API Gateway + Cognito for authentication/authorization
- Multi-region deployments with global failover














# ✅ Definition of Done & Quality Gates

This section defines the **success criteria** for development and delivery, ensuring the system meets both technical and business expectations.

---

### 📌 Functional Requirements
- `POST /orders`, `GET /orders/{id}`, `PATCH /orders/{id}`, and `/health` endpoints operational.
- Idempotency guaranteed on `POST` with consistent responses for retries.
- Optimistic locking enforced on `PATCH` with proper `409 Conflict` handling.
- State machine transitions validated with correct `422 Unprocessable Entity` errors.

---

### 🧪 Testing
- ✅ All unit and integration tests passing (`pytest` suite).
- ✅ Critical scenarios covered:
  - Idempotency retries
  - Version mismatch (`409`)
  - Invalid transitions (`422`)
- ✅ Coverage ≥ 70` (recommended target).

---

### 🧹 Code Quality
- ✅ Linting with Ruff → no critical issues.
- ✅ Formatting with Black → consistent style.
- ✅ Typing with Mypy → zero type errors.
- ✅ No silent exception swallowing (`try/except/pass` forbidden).
- ✅ Raise exceptions with context (`raise ... from e`).

---

### 🔍 Observability
- ✅ `/health` returns `200` when all dependencies are healthy, `503` otherwise.
- ✅ Structured JSON logs with `request_id`, `order_id`, `status`, and `latency`.
- ✅ Prometheus metrics exported (requests, state transitions, DB ops).

---

### 🛡️ Security
- ✅ Secrets never hardcoded in repo (managed via `.env` or secrets manager).
- ✅ Input validation and payload limits enforced.
- ✅ CORS restricted to trusted origins.
- ✅ Dependencies updated and scanned for vulnerabilities.

---

### 📄 Documentation & Assets
- ✅ README complete and professional (this document).
- ✅ `docs/API.md` with endpoint details and examples.
- ✅ `docs/ARCHITECTURE.md` explaining layers and decisions.
- ✅ `docs/AWS_ONE_PAGER.md` with production deployment reference.
- ✅ `docs/COMPLIANCE.md` mapping PCI-DSS/GDPR controls.
- ✅ `docs/DIAGRAMS/` with C4 and sequence diagrams.
- ✅ `docs/SLIDES/` with 3–6 slide pack for stakeholder presentation.

---

### 🚀 Delivery Workflow
- ✅ CI/CD pipeline runs: lint, tests, type checks, build.
- ✅ Docker images reproducible and versioned.
- ✅ Canary deployment and rollback strategy documented.
- ✅ Runbooks for common operational tasks.

---

> ✅ **Definition of Done**: All functional, quality, observability, security, and documentation criteria are satisfied, and the system is demonstrably ready for stakeholder review or production pilot.












# 📄 License / Authors / Links


### 📜 License
This project is released under the **MIT License**.  
You are free to use, modify, and distribute it with proper attribution.

---

### 👤 Author
Developed and maintained by **Hernando Silva Leal**  
- 🏷️ Also known as **NandoDev** — Specialist Backend Engineer  
- 🌐 Website: [www.nandodev.me](https://www.nandodev.me)  
- 💻 GitHub: [HernandoSilvaLeal](https://github.com/HernandoSilvaLeal/p1_talera)  
- 🔗 LinkedIn: [linkedin.com/in/nandosilvaleal](https://www.linkedin.com/in/nandosilvaleal/)  

---

### 🔗 Useful Links
- **API Reference** → `docs/API.md`  
- **Architecture Overview** → `docs/ARCHITECTURE.md`  
- **AWS One-Pager** → `docs/AWS_ONE_PAGER.md`  
- **Compliance Guidelines** → `docs/COMPLIANCE.md`  
- **Architectural Diagrams** → `docs/DIAGRAMS/`  
- **Slides for Stakeholders** → `docs/SLIDES/`  

---

> ✅ This documentation ensures that both technical and business stakeholders can quickly understand the purpose, architecture, and operational model of the **Order Processing Service**, and how it can be extended into **production-ready, serverless AWS environments**.
