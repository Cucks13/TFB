import os
from pathlib import Path
import importlib

import extract
import transform
import load

# Obtener la variable de entorno para la ruta de datos
DATA_PATH = os.getenv("DATA_PATH", "/app/data")

def load_scoring_modules():
    """Carga dinámicamente los módulos de scoring en la carpeta actual."""
    scoring_modules = {}
    scoring_path = Path(__file__).parent

    for file in scoring_path.glob("scoring_*.py"):
        module_name = file.stem  # Nombre del módulo sin extensión
        try:
            module = importlib.import_module(f"app.{module_name}")  # Importación correcta para Docker
            if hasattr(module, "run"):
                scoring_modules[module_name] = module.run
        except Exception as e:
            print(f"⚠️ Error al importar {module_name}: {e}")

    return scoring_modules

def main():
    print("🚀 Iniciando proceso ETL...")

    # Extracción de datos
    try:
        data = extract.run(DATA_PATH)
        print("✅ Extracción completada.")
    except Exception as e:
        print(f"❌ Error en extracción: {e}")
        return  # Salir si hay error crítico

    # Transformación de datos
    try:
        transformed_data = transform.run(data, DATA_PATH)
        print("✅ Transformación completada.")
    except Exception as e:
        print(f"❌ Error en transformación: {e}")
        return  # Salir si hay error crítico

    # Aplicar scoring
    try:
        scoring_modules = load_scoring_modules()
        for name, scoring_func in scoring_modules.items():
            transformed_data = scoring_func(transformed_data)
            print(f"✅ Scoring aplicado: {name}")
    except Exception as e:
        print(f"❌ Error en scoring: {e}")

    # Carga de datos
    try:
        load.run(transformed_data, DATA_PATH)
        print("✅ Carga completada.")
    except Exception as e:
        print(f"❌ Error en carga de datos: {e}")

    print("🎉 Proceso ETL finalizado con éxito.")

if __name__ == "__main__":
    main()
