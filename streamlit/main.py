import streamlit as st
from pymongo import MongoClient
import openai

# Configura tu clave de API de OpenAI
openai.api_key = "TU_API_KEY"  # Reemplaza con tu clave de API de OpenAI

# Conexión a MongoDB
def get_mongo_client():
    uri = "mongodb://localhost:27017/"  # Cambia esto si usas una URI remota (e.g., MongoDB Atlas)
    client = MongoClient(uri)
    return client

# Obtener las colecciones de la base de datos
def get_collections():
    client = get_mongo_client()
    db = client["wallapop"]  # Nombre de tu base de datos
    return db.list_collection_names()

# Mapeo de nombres técnicos a nombres amigables
COLLECTION_NAMES = {
    "data_niños_bebes": "Niños y Bebés",
    "data_industria_agricultura": "Industria y Agricultura",
    "data_tecnologia_electronica": "Tecnología y Electrónica",
    "data_inmobiliaria": "Inmobiliaria",
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

# Obtener documentos de una colección
def get_documents(collection_name):
    client = get_mongo_client()
    db = client["wallapop"]
    collection = db[collection_name]
    return list(collection.find().limit(20))  # Limitar a 20 documentos para evitar sobrecarga

# Mostrar documentos básicos
def mostrar_documentos_basicos(documentos):
    for doc in documentos:
        st.markdown("### 📦 Producto")
        st.write(f"- **ID del producto:** {doc.get('product_id', 'Sin ID')}")
        st.write(f"- **Descripción:** {doc.get('description', 'Sin descripción')}")
        st.write(f"- **Precio:** {doc.get('price', 'No disponible')} EUR")
        st.write(f"- **Ciudad:** {doc.get('ciudad', 'No disponible')}") 
        st.write(f"- **Score:** {doc.get('score', 'No disponible')}") 
        st.write(f"- **Enlace:** [Ver más detalles]({doc.get('url_completa', '#')})")
        st.divider()  # Separador visual entre documentos

# Chatbot de OpenAI
def chatbot_interface():
    st.markdown("### 🤖 Chatbot")
    st.write("Hazme preguntas sobre la colección o productos.")
    user_input = st.text_input("Tu pregunta:")
    if st.button("Enviar"):
        if user_input:
            with st.spinner("Pensando..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un asistente experto en productos de Wallapop."},
                        {"role": "user", "content": user_input},
                    ],
                )
                answer = response['choices'][0]['message']['content']
                st.write(f"**Chatbot:** {answer}")
        else:
            st.write("Por favor, escribe algo antes de enviar.")

# Aplicación principal
def main():
    st.title("Explorador de MongoDB - Wallapop")
    st.write("Esta aplicación muestra los datos de MongoDB.")

    # Mostrar las colecciones como botones en el menú lateral
    st.sidebar.title("Categorías")
    collections = get_collections()
    
    selected_collection = None
    for collection in collections:
        # Obtener el nombre amigable desde el diccionario
        friendly_name = COLLECTION_NAMES.get(collection, collection)
        if st.sidebar.button(friendly_name):
            selected_collection = collection

    # Mostrar documentos de la colección seleccionada
    if selected_collection:
        friendly_name = COLLECTION_NAMES.get(selected_collection, selected_collection)
        st.subheader(f"Documentos en la colección: {friendly_name}")
        documents = get_documents(selected_collection)
        if documents:
            mostrar_documentos_basicos(documents)
        else:
            st.write("No hay documentos en esta colección.")
        
        # Mostrar el chatbot
        chatbot_interface()
    else:
        st.write("Selecciona una colección en el menú lateral para explorar.")

if __name__ == "__main__":
    main()
