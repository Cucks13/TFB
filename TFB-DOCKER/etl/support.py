import os
import pandas as pd
import ast
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
import json

# Cargar variables de entorno
load_dotenv()

# Obtener valores de variables de entorno
DATA_PATH = os.getenv("DATA_PATH", "/app/data")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/etl_db")
KEY_WALLAPOP = os.getenv("KEY_WALLAPOP")

def traer_data(nombre_archivo, url):
    """Extrae datos desde la API de Wallapop y los guarda en CSV."""
    headers = {
        "x-rapidapi-key": KEY_WALLAPOP,
        "x-rapidapi-host": "wallapop3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        output_file = os.path.join(DATA_PATH, "raw", f"{nombre_archivo}.csv")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)

        print(f"✅ Datos guardados en {output_file}")
    else:
        print(f"❌ Error al obtener datos: {response.status_code}")

def process_multiple_csvs():
    """Procesa y limpia archivos CSV en una carpeta de entrada y guarda el resultado."""
    input_folder = os.path.join(DATA_PATH, "raw")
    output_folder = os.path.join(DATA_PATH, "coocked/csv")
    os.makedirs(output_folder, exist_ok=True)

    input_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.csv')]

    for input_file in input_files:
        try:
            df = pd.read_csv(input_file)
            
            if 'price' in df.columns:
                df['price'] = df['price'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else {"amount": None, "currency": None})
                df['amount'] = df['price'].apply(lambda x: x.get('amount', None))
                df['currency'] = df['price'].apply(lambda x: x.get('currency', None))

            if 'location' in df.columns:
                df['city'] = df['location'].apply(lambda x: ast.literal_eval(x).get('city', None))

            df.drop(columns=['price', 'location'], errors='ignore', inplace=True)

            output_file = os.path.join(output_folder, os.path.basename(input_file))
            df.to_csv(output_file, index=False)
            print(f"✅ Archivo procesado guardado en: {output_file}")

        except Exception as e:
            print(f"❌ Error al procesar {input_file}: {e}")

def convert_csv_to_json():
    """Convierte archivos CSV a JSON y los guarda en la carpeta adecuada."""
    input_folder = os.path.join(DATA_PATH, "coocked/csv")
    output_folder = os.path.join(DATA_PATH, "coocked/json")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            csv_path = os.path.join(input_folder, filename)
            try:
                df = pd.read_csv(csv_path)
                json_data = df.to_dict(orient="records")

                json_filename = os.path.splitext(filename)[0] + ".json"
                json_path = os.path.join(output_folder, json_filename)

                with open(json_path, "w", encoding="utf-8") as json_file:
                    json.dump(json_data, json_file, indent=4, ensure_ascii=False)
                
                print(f"✅ {filename} convertido a JSON: {json_path}")
            except Exception as e:
                print(f"❌ Error al convertir {filename} a JSON: {e}")

def insert_json_folder_to_mongo():
    """Inserta archivos JSON en MongoDB."""
    folder_path = os.path.join(DATA_PATH, "coocked/json/scoring")

    client = MongoClient(MONGO_URI)
    db = client["wallapop"]

    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            collection_name = os.path.splitext(file)[0]
            file_path = os.path.join(folder_path, file)

            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"❌ El archivo '{file}' no es un JSON válido. Saltando...")
                    continue

            if isinstance(data, list) and data:
                db[collection_name].insert_many(data)
                print(f"✅ Insertados {len(data)} documentos en '{collection_name}'")
            elif isinstance(data, dict):
                db[collection_name].insert_one(data)
                print(f"✅ Insertado 1 documento en '{collection_name}'")
            else:
                print(f"❌ El archivo '{file}' está vacío o tiene datos inválidos.")

