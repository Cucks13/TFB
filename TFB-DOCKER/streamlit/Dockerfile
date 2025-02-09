# Usa una imagen base ligera de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app.py /app/

# Definir variables de entorno
ENV MONGO_URI=mongodb://mongo:27017/etl_db

# Exponer el puerto 8501 para Streamlit
EXPOSE 8501

# Comando de ejecución
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
