import sys
sys.path.append("../")
from src import support as sp
import sys

# Paso 1
# Define la carpeta de entrada y salida para los archivos CSV
input_folder = "../data/raw/"
output_folder = "../data/coocked/csv"
# Procesa múltiples archivos CSV desde la carpeta de entrada y los guarda en la carpeta de salida
sp.process_multiple_csvs(input_folder, output_folder)


# Paso 2
# Define la carpeta de entrada y salida para la conversión de CSV a JSON
input_folder = "../data/coocked/csv"  # Cambia esto a la ruta de tu carpeta de entrada
output_folder = "../data/coocked/json"  # Cambia esto a la ruta de tu carpeta de salida
# Convierte los archivos CSV de la carpeta de entrada a archivos JSON en la carpeta de salida
sp.convert_csv_to_json(input_folder, output_folder)


# Paso 3
# Haremos un scoring de los productos de Wallapop para poder puntuarlos.
