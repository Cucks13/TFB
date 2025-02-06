import streamlit as st
from pymongo import MongoClient
import dotenv
import os
import time
from openai import OpenAI  # type: ignore

# Cargar variables de entorno desde .env
dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Verificar si la clave está configurada
if not api_key:
    st.error("No se encontró la clave de API en el archivo .env. Verifica la configuración.")
    st.stop()

# Configurar cliente OpenAI
cliente = OpenAI(api_key=api_key)

# ID del asistente personalizado
assistant_id = "asst_SOmHiZ04bWxZcFsQKpIxe1CE"

# Conexión a MongoDB
def get_mongo_client():
    uri = "mongodb://localhost:27017/"  # Cambia esto si usas una URI remota (e.g., MongoDB Atlas)
    client = MongoClient(uri)
    return client

# Obtener las colecciones de la base de datos
def get_collections():
    try:
        client = get_mongo_client()
        db = client["wallapop"]  # Nombre de tu base de datos
        return db.list_collection_names()
    except Exception as e:
        st.error(f"Error al conectar con MongoDB: {e}")
        return []

# Mapeo de nombres técnicos a nombres amigables
COLLECTION_NAMES = {
    "data_niños_bebes": "Niños y Bebés",
    "data_industria_agricultura": "Industria y Agricultura",
    "data_tecnologia_electronica": "Tecnología y Electrónica",
    "data_inmobilaria": "Inmobiliaria",
    "data_construccion_reforma": "Construcción y Reforma",
    "data_bicicleta": "Bicicletas",
    "data_electrodomesticos": "Electrodomésticos",
    "data_motos": "Motos",
    "data_deporte_ocio": "Deporte y Ocio",
    "data_moda_accesorios": "Moda y Accesorios",
    "data_cine_libros_musica": "Cine, Libros y Música",
    "data_hogar_jardin": "Hogar y Jardín",
    "data_coleccionismo": "Coleccionismo",
    "data_servicios": "Servicios",
    "data_otros": "Otros"
}

# Obtener documentos de una colección y ordenarlos por score de mayor a menor
def get_documents(collection_name):
    try:
        client = get_mongo_client()
        db = client["wallapop"]
        collection = db[collection_name]
        # Ordenar por 'score' en orden descendente y limitar a 20 documentos
        return list(collection.find().sort("score", -1).limit(20))
    except Exception as e:
        st.error(f"Error al obtener documentos de la colección '{collection_name}': {e}")
        return []

# Mostrar documentos básicos en contenedores
def mostrar_documentos_basicos(documentos):
    for doc in documentos:
        with st.container():
            st.markdown("### 📦 Producto")
            st.write(f"- **ID del producto:** {doc.get('product_id', 'Sin ID')}")
            st.write(f"- **Descripción:** {doc.get('description', 'Sin descripción')}") 
            st.write(f"- **Precio:** {doc.get('price', 'No disponible')} EUR")
            st.write(f"- **Ciudad:** {doc.get('ciudad', 'No disponible')}") 
            st.write(f"- **Score:** {doc.get('score', 'No disponible')}")
            
            url_completa = doc.get('url_completa', None)
            if url_completa:
                st.write(f"- **Enlace:** [Ver más detalles]({url_completa})")
            else:
                st.write("- **Enlace:** No disponible")
            st.divider()

# Chatbot con el asistente de OpenAI Assistants
def chatbot_interface():
    st.markdown("### 🤖 Chatbot")
    st.write("Hazme preguntas sobre la colección o productos.")

    # Crear hilo
    try:
        hilo = cliente.beta.threads.create()
        thread_id = hilo.id
        st.write("Se creó un hilo para esta conversación.")
    except Exception as e:
        st.error(f"Error al crear el hilo: {e}")
        return

    # Input del usuario
    mensaje = st.text_area("Escribe tu mensaje para el asistente:")

    # Botón para enviar mensaje
    if st.button("Enviar mensaje"):
        if mensaje.strip() == "":
            st.warning("Por favor, escribe un mensaje antes de enviarlo.")
        else:
            st.write("Procesando tu mensaje...")

            # Función para procesar datos
            def process_data(openai_client, assistant_id, thread_id, message):
                try:
                    # Enviar el mensaje al asistente
                    openai_client.beta.threads.messages.create(
                        thread_id=thread_id,
                        role="user",
                        content=message,
                    )

                    # Ejecutar el hilo con el asistente
                    run = openai_client.beta.threads.runs.create(
                        thread_id=thread_id,
                        assistant_id=assistant_id
                    )

                    # Esperar a que se complete la ejecución
                    while True:
                        run_status = openai_client.beta.threads.runs.retrieve(
                            thread_id=thread_id,
                            run_id=run.id
                        )
                        if run_status.status == "completed":
                            st.success("Se completó exitosamente.")
                            break
                        elif run_status.status == "failed":
                            st.error("Falló.")
                            break
                        else:
                            st.write("Esperando a que se complete...")
                            time.sleep(2)

                    # Obtener respuestas del asistente
                    response_messages = openai_client.beta.threads.messages.list(thread_id=thread_id)

                    assistant_response = None
                    for message in response_messages.data:
                        if message.role == "assistant":
                            assistant_response = "\n".join([block.text.value for block in message.content])
                            break

                    if assistant_response:
                        return assistant_response
                    else:
                        return "No se encontró una respuesta del asistente."

                except Exception as e:
                    st.error(f"Error al procesar los datos: {e}")
                    return None

            # Procesar el mensaje
            respuesta = process_data(cliente, assistant_id, thread_id, mensaje)

            # Mostrar la respuesta
            if respuesta:
                st.write("### Respuesta del asistente:")
                st.write(respuesta)
            else:
                st.error("No se pudo obtener una respuesta del asistente.")

# Aplicación principal
def main():
    st.title("Explorador de MongoDB - Wallapop")

    # Sidebar: Menú de categorías
    st.sidebar.title("Categorías")
    collections = get_collections()
    if not collections:
        st.sidebar.warning("No se encontraron colecciones en la base de datos.")
        return

    # Botones para seleccionar la colección
    selected_collection = None
    for collection in collections:
        friendly_name = COLLECTION_NAMES.get(collection, collection)
        if st.sidebar.button(friendly_name):
            selected_collection = collection

    # Dividir pantalla en dos columnas (productos y chatbot)
    col1, col2 = st.columns([2, 2])  # Ajustar proporciones según tu preferencia
 
    # Mostrar productos en col1
    with col1:
        if selected_collection:
            friendly_name = COLLECTION_NAMES.get(selected_collection, selected_collection)
            st.subheader(f"Documentos en la colección: {friendly_name}")
            documents = get_documents(selected_collection)
            if documents:
                mostrar_documentos_basicos(documents)
            else:
                st.warning("No hay documentos en esta colección.")
        else:
            st.write("Selecciona una categoría en el menú lateral para explorar.")

    # Mostrar chatbot en col2
    with col2:
        chatbot_interface()

if __name__ == "__main__":
    main()
