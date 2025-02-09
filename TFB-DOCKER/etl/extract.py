"""
Este script extrae datos desde la API de Wallapop para diferentes categorías de productos.
Usa `traer_data` del módulo `support` y almacena los datos en `DATA_PATH/raw/`.
"""

import os
from etl import support as sp  
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
DATA_PATH = os.getenv("DATA_PATH", "/app/data")
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw")

# Crear carpeta si no existe
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# Definir categorías y URLs
CATEGORIAS = {
    "data_coches": "https://es.wallapop.com/app/search?category_ids=100",
    "data_motos": "https://es.wallapop.com/app/search?category_ids=14000",
    "data_moda_accesorios": "https://es.wallapop.com/app/search?category_ids=12465",
    "data_inmobilaria": "https://es.wallapop.com/app/search?category_ids=200",
    "data_tecnologia_electronica": "https://es.wallapop.com/app/search?category_ids=24200",
    "data_deporte_ocio": "https://es.wallapop.com/app/search?category_ids=12579",
    "data_bicibleta": "https://es.wallapop.com/app/search?category_ids=17000",
    "data_hogar_jardin": "https://es.wallapop.com/app/search?category_ids=12467",
    "data_electrodomesticos": "https://es.wallapop.com/app/search?category_ids=12467",
    "data_cine_libros_musica": "https://es.wallapop.com/app/search?category_ids=12463",
    "data_nilos_bebes": "https://es.wallapop.com/app/search?category_ids=12461",
    "data_coleccionismo": "https://es.wallapop.com/app/search?category_ids=18000",
    "data_construccion_reforma": "https://es.wallapop.com/app/search?category_ids=19000",
    "data_industria_agricultura": "https://es.wallapop.com/app/search?category_ids=20000",
    "data_servicios": "https://es.wallapop.com/app/search?category_ids=13200",
    "data_otros": "https://es.wallapop.com/app/search?category_ids=12485",
}

if __name__ == "__main__":
    print("🚀 Iniciando extracción de datos...")

    for nombre_archivo, url in CATEGORIAS.items():
        print(f"📥 Extrayendo: {nombre_archivo}...")
        sp.traer_data(nombre_archivo, url)

    print("✅ Extracción completada.")
