# Imagen base oficial de Python
FROM python:3.11-slim

# Evita mensajes de buffer y bytecode
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cache
COPY requirements.txt .

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copiar el código de la app
COPY app ./app

# Exponer el puerto (ajustado a tu configuración)
EXPOSE 8081

# Comando de arranque
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]
