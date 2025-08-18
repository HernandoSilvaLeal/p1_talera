FROM python:3.11-slim

WORKDIR /app

# Copiar solo los archivos de dependencias primero para aprovechar el cache de Docker
COPY pyproject.toml poetry.lock* ./

# Configurar Poetry para no usar venv y luego instalar dependencias
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install --no-cache-dir poetry && poetry install --only main --no-root

# Copiar el resto de la aplicación
COPY . .

# El CMD por defecto para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
