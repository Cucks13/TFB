import json
import os

# Funciones para evaluar la calidad de la descripción y el precio
def evaluar_descripcion(descripcion):
    """Evalúa la descripción del producto según su longitud y palabras clave."""
    score = 0

    # Evaluación por longitud de la descripción
    if len(descripcion) > 150:
        score += 5
    elif len(descripcion) > 100:
        score += 4
    elif len(descripcion) > 50:
        score += 3
    else:
        score += 1

    # Evaluación por palabras clave
    palabras_clave = ["nuevo", "en perfecto estado", "sin abrir"]
    if any(palabra in descripcion.lower() for palabra in palabras_clave):
        score += 2

    return score

def evaluar_precio(precio):
    """Evalúa el precio del producto y asigna un puntaje."""
    if precio < 50:
        return 5
    elif precio < 150:
        return 4
    elif precio < 500:
        return 3
    elif precio < 1000:
        return 2
    else:
        return 1

def cargar_productos(ruta_archivo):
    """Carga productos desde un archivo JSON."""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {ruta_archivo}")
        return []
    except json.JSONDecodeError:
        print("Error: El archivo no contiene un JSON válido")
        return []

def guardar_resultados(resultados, ruta_salida):
    """Guarda los resultados en un archivo JSON."""
    try:
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        with open(ruta_salida, 'w', encoding='utf-8') as file:
            json.dump(resultados, file, indent=2, ensure_ascii=False)
        print(f"Archivo guardado exitosamente en: {ruta_salida}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

def procesar_productos(ruta_archivo, ruta_salida):
    """Procesa los productos, evalúa su descripción y precio, y guarda los resultados."""
    productos = cargar_productos(ruta_archivo)

    if not productos:
        print("No se encontraron productos para procesar.")
        return

    resultados = []
    for producto in productos:
        try:
            descripcion_score = evaluar_descripcion(producto.get("description", ""))
            precio_score = evaluar_precio(producto.get("amount", 0))
            puntaje_total = descripcion_score + precio_score

            resultados.append({
                "product_id": producto.get("id"),
                "user_id": producto.get("user_id"),
                "description": producto.get("description", ""),
                "price": f"{producto.get('amount', 0)} {producto.get('currency', 'N/A')}",
                "taxonomy": producto.get("taxonomy", "N/A"),
                "reservado": producto.get("reservado", False),
                "envio": producto.get("envio", False),
                "url_completa": producto.get("url_completa", ""),
                "ciudad": producto.get("ciudad", ""),
                "score": min(puntaje_total, 10)
            })
        except Exception as e:
            print(f"Error al procesar el producto con ID {producto.get('id')}: {e}")

    guardar_resultados(resultados, ruta_salida)
    print(json.dumps(resultados, indent=2, ensure_ascii=False))

# Rutas de ejemplo (cambiar según sea necesario)
ruta_archivo = '../data/coocked/json/data_bicicleta.json'
ruta_salida = '../data/coocked/json/scoring/data_bicicleta.json'

# Procesar productos 
procesar_productos(ruta_archivo, ruta_salida)
