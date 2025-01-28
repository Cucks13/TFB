import streamlit as st
from pymongo import MongoClient

# Conexión a MongoDB
def get_mongo_client():
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    return client

# Obtener las colecciones de la base de datos
def get_collections():
    client = get_mongo_client()
    db = client["wallapop"]
    return db.list_collection_names()

# Obtener documentos de una colección
def get_documents(collection_name):
    client = get_mongo_client()
    db = client["wallapop"]
    collection = db[collection_name]
    return list(collection.find().limit(20))  # Limitar a 20 documentos

# Mostrar documentos con un diseño claro
def mostrar_documentos(documentos):
    for doc in documentos:
        with st.container():
            # Título
            st.markdown(f"### 📦 {doc.get('title', 'Sin título')}")
            
            # Descripción
            st.write(doc.get("description", "Sin descripción"))
            
            # Precio
            price = doc.get("amount", "N/A")
            currency = doc.get("currency", "")
            st.write(f"💰 **Precio:** {price} {currency}")
            
            # Ubicación (solo campos relevantes)
            location = doc.get("location", {})
            city = location.get("city", "Sin ciudad")
            region = location.get("region", "Sin región")
            st.write(f"📍 **Ubicación:** {city}, {region}")
            
            # Categorías o taxonomía
            taxonomy = doc.get("taxonomy", [])
            if taxonomy:
                categories = ", ".join([t.get("name", "Sin categoría") for t in taxonomy])
                st.write(f"🏷️ **Categorías:** {categories}")
            
            # Estado de reservado y envío
            reserved = doc.get("reserved", False)
            shipping = doc.get("shipping", False)
            st.write(f"🔒 **Reservado:** {'Sí' if reserved else 'No'}")
            st.write(f"🚚 **Envío disponible:** {'Sí' if shipping else 'No'}")
            
            # Enlace al producto
            url = doc.get("url_completa", "#")
            st.markdown(f"🔗 [Ver más detalles]({url})")
            
            st.divider()  # Línea divisoria entre documentos

# Aplicación principal
def main():
    st.title("Explorador de MongoDB - Wallapop")

    # Obtener las colecciones
    collections = get_collections()

    # Menú horizontal con botones
    st.markdown("### Selecciona una colección:")
    selected_collection = None
    cols = st.columns(len(collections))  # Crear una columna por cada colección

    for col, collection in zip(cols, collections):
        if col.button(collection):
            selected_collection = collection

    # Mostrar documentos de la colección seleccionada
    if selected_collection:
        st.subheader(f"Documentos en la colección: {selected_collection}")
        documents = get_documents(selected_collection)
        if documents:
            mostrar_documentos(documents)
        else:
            st.write("No hay documentos en esta colección.")
    else:
        st.write("Haz clic en una colección para explorarla.")

if __name__ == "__main__":
    main()
