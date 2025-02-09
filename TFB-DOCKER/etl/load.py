import os
from etl import support as sp

DATA_PATH = os.getenv("DATA_PATH", "/app/data")
json_folder = os.path.join(DATA_PATH, "coocked/json/scoring")

sp.insert_json_folder_to_mongo(json_folder)
