import sys
sys.path.append("../")
from src import support as sp

# Paso 1
# Ejecutamos la insercción de los archivos JSON a la base de datos de MongoDB
sp.insert_json_folder_to_mongo("../data/coocked/json/scoring")