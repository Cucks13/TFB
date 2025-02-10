import streamlit as st
from pymongo import MongoClient
import dotenv
import pandas as pd
import os
import time
from openai import OpenAI
# Cargar variables de entorno desde .env
dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Verificar si la clave de API es válida
if not api_key:
    st.error("No se encontró la clave de API en el archivo .env. Verifica la configuración.")
    st.stop()
# Configurar cliente OpenAI
cliente = OpenAI(api_key=api_key)
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
# Obtener documentos de una colección y ordenarlos por score de mayor a menor
def get_documents(collection_name):
    try:
        client = get_mongo_client()
        db = client["wallapop"]
        collection = db[collection_name]
        return list(collection.find().sort("score", -1).limit(20))
    except Exception as e:
        st.error(f"Error al obtener documentos de la colección '{collection_name}': {e}")
        return []
# Mostrar documentos básicos en contenedores
def mostrar_documentos_basicos(documentos):
    for doc in documentos:
        with st.container():
            st.markdown("### Producto")
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
# Chatbot simple con OpenAI sin asistente
def chatbot_interface_simple(df, collection_name):
    st.markdown("### 🤖 Chatbot")
    st.write("Hazme preguntas sobre la colección o productos.")
    # Contexto adicional del dataset y colección
    context_data = f"Análisis de la colección: {collection_name}\n\nDatos:\n{df.head().to_string()}"
    mensaje = st.text_area("Escribe tu mensaje para el chatbot:")
    # Botón para enviar mensaje
    if st.button("Enviar mensaje"):
        if mensaje.strip() == "":
            st.warning("Por favor, escribe un mensaje antes de enviarlo.")
        else:
            st.write("Procesando tu mensaje...")
            prompt = f"""
Datos de la colección seleccionada:
{context_data}
Pregunta del usuario: {mensaje}
Por favor, responde de manera precisa y basada en los datos proporcionados.
"""
            try:
                response = cliente.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un asistente experto en productos y análisis de datos."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.1,
                )
                respuesta = response.choices[0].message.content
                st.write("### Respuesta del chatbot:")
                st.write(respuesta)
            except Exception as e:
                st.error(f"Error al procesar los datos: {e}")
# Aplicación principal
def main():
    st.set_page_config(layout="wide", page_title="Explorador de MongoDB con Chatbot")
    st.title("Wallapop - Product search")
    # Sidebar: Menú de categorías como botones
    st.sidebar.title("Categorías")
    collections = get_collections()
    if not collections:
        st.sidebar.warning("No se encontraron colecciones en la base de datos.")
        return
    selected_collection = None
    for collection in collections:
        friendly_name = collection.replace("data_", "").replace("_", " ").capitalize()
        if st.sidebar.button(friendly_name):
            selected_collection = collection
    # Selección de colección
    selected_collection = st.sidebar.radio("Selecciona una categoría:", collections)
    # Dividir pantalla en dos columnas (productos y chatbot)
    col1, col2 = st.columns([3, 2])  # Ajustar proporciones para más espacio al chatbot
    # Mostrar productos en col1
    with col1:
        if selected_collection:
            st.subheader(f"Documentos en la colección: {selected_collection}")
            documents = get_documents(selected_collection)
            if documents:
                mostrar_documentos_basicos(documents)
            else:
                st.warning("No hay documentos en esta colección.")
        else:
            st.write("Selecciona una categoría en el menú lateral para explorar.")
    # Mostrar chatbot en col2
    with col2:
        if selected_collection:
            df = pd.DataFrame(get_documents(selected_collection))
            chatbot_interface_simple(df, selected_collection)
        else:
            st.write("Selecciona una categoría para interactuar con el chatbot.")
if __name__ == "__main__":
    main()