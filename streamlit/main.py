import streamlit as st
import time
import os
import sys
sys.path.append("../../")
import dotenv
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

# ID del asistente (Especificado manualmente)
assistant_id = "asst_SOmHiZ04bWxZcFsQKpIxe1CE"

# Título de la aplicación
st.title("Asistente AI con OpenAI Assistants")
st.write(f"Asistente seleccionado: {assistant_id}")

# Crear hilo
try:
    hilo = cliente.beta.threads.create()
    thread_id = hilo.id
    st.write("Se creó un hilo para esta conversación.")
except Exception as e:
    st.error(f"Error al crear el hilo: {e}")
    st.stop()

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