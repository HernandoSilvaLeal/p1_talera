# --- Etapa 1: Builder ---
# Instala dependencias en un entorno virtual aislado.
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# 1. Instalar poetry
RUN pip install poetry

# 2. Copiar solo los archivos de dependencias para aprovechar el cache de Docker
COPY pyproject.toml poetry.lock* ./

# 3. Instalar dependencias de producción
RUN poetry install --without dev --no-root

# --- Etapa 2: Final ---
# Copia el entorno virtual y el código de la aplicación a una imagen limpia.
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# 1. Copiar el entorno virtual del builder
COPY --from=builder /app/.venv ./.venv

# 2. Activar el entorno virtual para los comandos siguientes
ENV PATH="/app/.venv/bin:$PATH"

# 3. Copiar el código de la aplicación
COPY ./app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
