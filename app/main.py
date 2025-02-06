import extract
import transform
import load
import os

# Importar dinámicamente los módulos de scoring
from pathlib import Path
import importlib

def load_scoring_modules():
    scoring_modules = {}
    scoring_path = Path(__file__).parent
    for file in scoring_path.glob("scoring_*.py"):
        module_name = file.stem  # Nombre del módulo sin extensión
        try:
            scoring_modules[module_name] = importlib.import_module(module_name)
        except ModuleNotFoundError as e:
            print(f"Error al importar {module_name}: {e}")
    return scoring_modules

def main():
    print("Iniciando proceso ETL...")
    
    # Extracción de datos
    data = extract.run()
    print("Extracción completada.")
    
    # Transformación de datos
    transformed_data = transform.run(data)
    print("Transformación completada.")
    
    # Aplicar scoring
    scoring_modules = load_scoring_modules()
    for name, module in scoring_modules.items():
        if hasattr(module, 'run'):
            transformed_data = module.run(transformed_data)
            print(f"Scoring aplicado: {name}")
    
    # Carga de datos
    load.run(transformed_data)
    print("Carga completada.")
    
    print("Proceso ETL finalizado con éxito.")

if __name__ == "__main__":
    main()
