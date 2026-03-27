FROM python:3.12

WORKDIR /app

# Argumento con la ruta local del archivo de requerimientos
ARG requirements=requirements/reqs.txt

# Copiar el archivo de requerimientos tal cual (sin renombrar)
COPY ${requirements} ./reqs.txt

# Instalar dependencias desde reqs.txt
RUN pip install --no-cache-dir -r reqs.txt

# Copiar el resto del código
COPY . .

EXPOSE 8001

# Comando por defecto (será sobrescrito en docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]