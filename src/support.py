import os
import pandas as pd
import ast
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
import json


# Cargar el archivo .env
load_dotenv()

# Acceder a las variables de entorno
KEY_WALLAPOP = os.getenv("KEY_WALLAPOP")

# Imprimir las variables para verificar que están cargadas

def traer_data(nombre_archivo, url):
    # Encabezados de la API
    headers = {
        "x-rapidapi-key": KEY_WALLAPOP,  # Reemplaza con tu clave
        "x-rapidapi-host": "wallapop3.p.rapidapi.com"
    }

    # Solicitar los datos de la API
    response = requests.get(url, headers=headers)

    # Asegurarse de que la respuesta es válida
    if response.status_code == 200:
        data = response.json()  # Convertir la respuesta a JSON
        # Crear un DataFrame a partir de la lista de diccionarios
        df = pd.DataFrame(data)
        
        # Guardar los datos en un archivo CSV
        df.to_csv(f"../data/{nombre_archivo}.csv", index=False)
        print(f"Datos guardados en {nombre_archivo}.csv")
    else:
        print(f"Error al obtener datos: {response.status_code}")




def process_multiple_csvs(input_folder, output_folder):
    """
    Procesa todos los archivos CSV en una carpeta de entrada y guarda los resultados en la carpeta de salida.
    
    :param input_folder: Carpeta donde se encuentran los archivos CSV de entrada.
    :param output_folder: Carpeta donde se guardarán los archivos procesados.
    """
    # Listar todos los archivos CSV en la carpeta de entrada
    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.csv')]
    
    # Iterar sobre cada archivo y procesarlo
    for input_file in input_files:
        try:
            # Cargar el archivo CSV
            df = pd.read_csv(input_file)
            
            # Paso 1: Procesar la columna 'price'
            try:
                if 'price' in df.columns:
                    df['price'] = df['price'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else {"amount": None, "currency": None})
                    df['amount'] = df['price'].apply(lambda x: x.get('amount', None))
                    df['currency'] = df['price'].apply(lambda x: x.get('currency', None))
            except Exception as e:
                print(f"Error procesando 'price' en {input_file}: {e}")
            
            # Paso 2: Procesar la columna 'reserved'
            try:
                if 'reserved' in df.columns:
                    df['reserved'] = df['reserved'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else {"flag": None})
                    df['flag'] = df['reserved'].apply(lambda x: x.get('flag', None))
            except Exception as e:
                print(f"Error procesando 'reserved' en {input_file}: {e}")

            # Paso 3: Procesar la columna 'shipping'
            try:
                if 'shipping' in df.columns:
                    df['shipping'] = df['shipping'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else {"user_allows_shipping": None})
                    df['user_allows_shipping'] = df['shipping'].apply(lambda x: x.get('user_allows_shipping', None))
            except Exception as e:
                print(f"Error procesando 'shipping' en {input_file}: {e}")

            # Paso 4: Crear la columna 'url_completa'
            try:
                if 'web_slug' in df.columns:
                    df['url_completa'] = "https://es.wallapop.com/item/" + df['web_slug']
            except Exception as e:
                print(f"Error procesando 'web_slug' en {input_file}: {e}")


            # Paso 5: Crear la columna 'ciudad', extaryendo la clave 'city' de la columna 'location'
            df['city'] = df['location'].apply(lambda x: ast.literal_eval(x)['city'])
            
            # Paso 6: Eliminar columnas no necesarias
            columns_to_drop = [
                "images", "price", "shipping", "bump", "web_slug", "reserved", "favorited",
                "created_at", "modified_at", "discount", "category_id", "is_favoriteable",
                "is_refurbished", "location"
            ]
            for column in columns_to_drop:
                if column in df.columns:
                    df.drop(column, axis=1, inplace=True)

            # Paso 7: Renombrar columnas
            df.rename(columns={
                "flag": "reservado",
                "user_allows_shipping": "envio",
                "city": "ciudad"
            }, inplace=True)
            
            # Paso 8: Guardar el archivo procesado
            # Obtener el nombre del archivo original
            filename = os.path.basename(input_file)
            # Crear la ruta completa para guardar el archivo procesado
            output_file = os.path.join(output_folder, filename)
            # Guardar el archivo en formato CSV
            df.to_csv(output_file, index=False)
            
            print(f"Archivo procesado guardado en: {output_file}")
        
        except Exception as e:
            print(f"Error al procesar el archivo {input_file}: {e}")




# Función para procesar todos los CSV de una carpeta y crear colecciones en MongoDB
import os
from pymongo import MongoClient
import json

def insert_json_folder_to_mongo(folder_path, db_name="wallapop", mongo_uri="mongodb://localhost:27017/"):
    """
    Inserta todos los archivos JSON de una carpeta en MongoDB.
    
    Args:
        folder_path (str): Ruta de la carpeta que contiene los archivos JSON.
        db_name (str): Nombre de la base de datos en MongoDB.
        mongo_uri (str): URI de conexión a MongoDB.
        
    Returns:
        None
    """
    # Conexión a MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    
    # Procesar cada archivo en la carpeta
    for file in os.listdir(folder_path):
        if file.endswith(".json"):  # Solo procesar archivos JSON
            collection_name = os.path.splitext(file)[0]  # Nombre de colección = nombre del archivo
            file_path = os.path.join(folder_path, file)  # Ruta completa al archivo
            
            # Leer el JSON y cargarlo como lista de documentos
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)  # Cargar el contenido del archivo JSON
                except json.JSONDecodeError:
                    print(f"El archivo '{file}' no es un JSON válido. Saltando...")
                    continue
            
            # Verificar si los datos son una lista de documentos
            if isinstance(data, list) and data:
                db[collection_name].insert_many(data)
                print(f"Insertados {len(data)} documentos en la colección '{collection_name}'")
            elif isinstance(data, dict):  # Si el JSON es un objeto único
                db[collection_name].insert_one(data)
                print(f"Insertado 1 documento en la colección '{collection_name}'")
            else:
                print(f"El archivo '{file}' está vacío o no contiene datos válidos para insertar.")

    print("Inserción completada.")

                
# Función para convertir todos los archivos CSV en una carpeta a archivos JSON
def convert_csv_to_json(input_folder, output_folder):
    """
    Convierte todos los archivos CSV en una carpeta a archivos JSON y los guarda en otra carpeta.
    
    Args:
        input_folder (str): Ruta de la carpeta que contiene los archivos CSV.
        output_folder (str): Ruta de la carpeta donde se guardarán los archivos JSON.
    """
    # Asegúrate de que la carpeta de salida existe
    os.makedirs(output_folder, exist_ok=True)

    # Iterar sobre todos los archivos en la carpeta de entrada
    for filename in os.listdir(input_folder):
        # Comprobar si el archivo tiene extensión .csv
        if filename.endswith(".csv"):
            csv_path = os.path.join(input_folder, filename)
            
            # Leer el CSV
            try:
                df = pd.read_csv(csv_path)
            except Exception as e:
                print(f"Error al leer {filename}: {e}")
                continue
            
            # Convertir a JSON
            json_data = df.to_dict(orient="records")
            
            # Nombre del archivo de salida
            json_filename = os.path.splitext(filename)[0] + ".json"
            json_path = os.path.join(output_folder, json_filename)
            
            # Guardar como JSON
            try:
                with open(json_path, "w", encoding="utf-8") as json_file:
                    json.dump(json_data, json_file, indent=4, ensure_ascii=False)
                print(f"{filename} convertido a {json_filename}")
            except Exception as e:
                print(f"Error al guardar {json_filename}: {e}")