import os
from etl import support as sp

DATA_PATH = os.getenv("DATA_PATH", "/app/data")

if __name__ == "__main__":
    print("🚀 Iniciando transformación de datos...")
    sp.process_multiple_csvs()
    sp.convert_csv_to_json()
    print("✅ Transformación completada.")

