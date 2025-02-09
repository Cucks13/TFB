# Readme proyecto dockerizado

# **📌 Documentación: Implementación de la ETL y Streamlit con Docker**

## **1️⃣ Introducción**

Este documento describe la configuración, implementación y despliegue de una **ETL** que extrae, transforma y carga datos en **MongoDB**, junto con una aplicación **Streamlit** que consume estos datos.

Se utiliza **Docker** para crear contenedores separados para cada servicio:
✅ **ETL**: Procesa los datos de Wallapop y los almacena en MongoDB.

✅ **MongoDB**: Base de datos NoSQL para almacenar la información procesada.

✅ **Mongo Express**: Interfaz gráfica para gestionar MongoDB.

✅ **Streamlit**: Interfaz web para visualizar los datos y usar un chatbot con OpenAI.

---

## **2️⃣ Estructura del Proyecto**

El proyecto se organiza en la siguiente estructura de carpetas:

```
tfb-docker/
│── .env                 # Variables de entorno (MongoDB, API Keys, etc.)
│── .gitignore           # Evita subir `.env` y `data/`
│── docker-compose.yml   # Orquestación de los contenedores
│── etl/                 # Carpeta de la ETL
│   │── Dockerfile       # Dockerfile de la ETL
│   │── requirements.txt # Dependencias de la ETL
│   │── extract.py       # Extracción de datos
│   │── transform.py     # Transformación de datos
│   │── load.py          # Carga en MongoDB
│   │── main.py          # Orquestación del flujo ETL
│── streamlit/           # Carpeta de la app Streamlit
│   │── Dockerfile       # Dockerfile de Streamlit
│   │── requirements.txt # Dependencias de Streamlit
│   │── app.py           # Código principal de la aplicación
│── data/                # Carpeta donde se almacenan los datos procesados
```

---

## **3️⃣ Configuración de Variables de Entorno (`.env`)**

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
# Configuración de MongoDB
MONGO_URI=mongodb://mongo:27017/etl_db

# Ruta de almacenamiento de datos
DATA_PATH=/app/data

# API Key de Wallapop
KEY_WALLAPOP=tu_api_key_aqui

# Credenciales de Mongo Express
MONGO_EXPRESS_USER=admin
MONGO_EXPRESS_PASSWORD=password
```

⚠️ **Importante:** Agregar `.env` al `.gitignore` para no subir credenciales sensibles.

```
.env
data/
```

---

## **4️⃣ Configuración de Docker**

### **🔹 4.1 Dockerfile para la ETL (`etl/Dockerfile`)**

```
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
ENV DATA_PATH=/app/data
ENV MONGO_URI=mongodb://mongo:27017/etl_db
RUN mkdir -p $DATA_PATH/raw $DATA_PATH/coocked/json $DATA_PATH/coocked/csv
CMD ["python", "main.py"]
```

### **🔹 4.2 Dockerfile para Streamlit (`streamlit/Dockerfile`)**

```
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py /app/
ENV MONGO_URI=mongodb://mongo:27017/etl_db
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **🔹 4.3 `docker-compose.yml` (en la raíz del proyecto)**

```yaml
version: "3.8"
services:
  etl:
    build: ./etl
    container_name: etl_pipeline
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    depends_on:
      - mongo
    networks:
      - shared_network
    command: ["python", "main.py"]

  mongo:
    image: mongo:5.0
    container_name: etl_mongo
    restart: always
    environment:
      MONGO_INITDB_DATABASE: etl_db
    ports:
      - "27017:27017"
    networks:
      - shared_network
    volumes:
      - mongo_data:/data/db

  mongo-express:
    image: mongo-express
    container_name: etl_mongo_express
    restart: always
    environment:
      ME_CONFIG_MONGODB_SERVER: mongo
      ME_CONFIG_MONGODB_PORT: 27017
      ME_CONFIG_BASICAUTH_USERNAME: ${MONGO_EXPRESS_USER}
      ME_CONFIG_BASICAUTH_PASSWORD: ${MONGO_EXPRESS_PASSWORD}
    ports:
      - "8081:8081"
    depends_on:
      - mongo
    networks:
      - shared_network

  streamlit:
    build: ./streamlit
    container_name: streamlit_app
    ports:
      - "8501:8501"
    env_file:
      - .env
    depends_on:
      - mongo
    networks:
      - shared_network

networks:
  shared_network:

volumes:
  mongo_data:
```

---

## **5️⃣ Despliegue y Ejecución**

### **1️⃣ Construir los Contenedores**

```bash
docker-compose build
```

### **2️⃣ Levantar los Contenedores**

```bash
docker-compose up -d
```

### **3️⃣ Verificar que Todo Funciona**

- **Mongo Express** 👉 `http://localhost:8081`
- **Streamlit** 👉 `http://localhost:8501`

### **4️⃣ Ver los Logs**

```bash
docker-compose logs -f etl
docker-compose logs -f streamlit
```

---

## **📌 Conclusión**

✅ **Cada servicio tiene su propio `Dockerfile` y está separado correctamente.**

✅ **El `docker-compose.yml` en la raíz orquesta toda la infraestructura.**

✅ **MongoDB está accesible para ambos servicios a través de `shared_network`.**

✅ **Puedes reiniciar Streamlit o la ETL sin afectar al otro.**