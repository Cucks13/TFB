FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar y cargar las variables de entorno desde .env
COPY .env /app/.env

# Copiar dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la ETL
COPY app/ /app/

# Crear directorios de datos dentro del contenedor
ENV DATA_PATH=/app/data
RUN mkdir -p $DATA_PATH/raw $DATA_PATH/coocked/json $DATA_PATH/coocked/csv

# Definir variables de entorno por defecto
ENV MONGO_URI=mongodb://mongo:27017/etl_db

# Cargar variables desde .env
RUN python -c "from dotenv import load_dotenv; load_dotenv('.env')"

# Comando de ejecución
CMD ["python", "main.py"]