"""
Este script se encarga de la extracción de datos desde la API de Wallapop para diferentes categorías de productos.
Utiliza la función `traer_data` del módulo `support` para realizar las solicitudes a la API y guardar los datos obtenidos.
Funciones:
    - sp.traer_data(nombre_archivo, url): Realiza una solicitud a la API de Wallapop y guarda los datos en un archivo.
Categorías de productos y sus respectivas URLs:
    - data_coches: "https://es.wallapop.com/app/search?category_ids=100&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_motos: "https://es.wallapop.com/app/search?category_ids=14000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_moda_accesorios: "https://es.wallapop.com/app/search?category_ids=12465&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_inmobilaria: "https://es.wallapop.com/app/search?category_ids=200&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_tecnologia_electronica: "https://es.wallapop.com/app/search?category_ids=24200&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_deporte_ocio: "https://es.wallapop.com/app/search?category_ids=12579&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_bicibleta: "https://es.wallapop.com/app/search?category_ids=17000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_hogar_jardin: "https://es.wallapop.com/app/search?category_ids=12467&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_electrodomesticos: "https://es.wallapop.com/app/search?category_ids=12467&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_cine_libros_musica: "https://es.wallapop.com/app/search?category_ids=12463&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_nilos_bebes: "https://es.wallapop.com/app/search?category_ids=12461&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_coleccionismo: "https://es.wallapop.com/app/search?category_ids=18000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_construccion_reforma: "https://es.wallapop.com/app/search?category_ids=19000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_industria_agricultura: "https://es.wallapop.com/app/search?category_ids=20000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_servicios: "https://es.wallapop.com/app/search?category_ids=13200&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
    - data_otros: "https://es.wallapop.com/app/search?category_ids=12485&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters"
"""
import sys
sys.path.append("../")
from src import support as sp

# Extraccion de los datos, en este caso, los datos vienen de la API de Wallapop.
sp.traer_data("data_coches", "https://es.wallapop.com/app/search?category_ids=100&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_motos", "https://es.wallapop.com/app/search?category_ids=14000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_moda_accesorios", "https://es.wallapop.com/app/search?category_ids=12465&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_inmobilaria", "https://es.wallapop.com/app/search?category_ids=200&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_tecnologia_electronica", "https://es.wallapop.com/app/search?category_ids=24200&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_deporte_ocio", "https://es.wallapop.com/app/search?category_ids=12579&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_bicibleta", "https://es.wallapop.com/app/search?category_ids=17000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_hogar_jardin", "https://es.wallapop.com/app/search?category_ids=12467&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_electrodomesticos", "https://es.wallapop.com/app/search?category_ids=12467&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_cine_libros_musica", "https://es.wallapop.com/app/search?category_ids=12463&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_nilos_bebes", "https://es.wallapop.com/app/search?category_ids=12461&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_coleccionismo", "https://es.wallapop.com/app/search?category_ids=18000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_construccion_reforma", "https://es.wallapop.com/app/search?category_ids=19000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_industria_agricultura", "https://es.wallapop.com/app/search?category_ids=20000&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_servicios", "https://es.wallapop.com/app/search?category_ids=13200&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")
sp.traer_data("data_otros", "https://es.wallapop.com/app/search?category_ids=12485&latitude=40.41956&longitude=-3.69196&filters_source=side_bar_filters")

