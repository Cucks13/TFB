import json
import random
import os

# Definición de precios de referencia
precios_referencia = {
    "collectibles": [0.22, 5.0, 20.0, 4.0, 12.0, 10.0, 30.0, 40.0, 225.0, 4400.0],
}

def evaluar_descripcion(descripcion):
    score = 0
    # Variar la puntuación de longitud
    if len(descripcion) > 150:
        score += random.randint(4, 6)
    elif len(descripcion) > 100:
        score += random.randint(3, 5)
    elif len(descripcion) > 50:
        score += random.randint(2, 4)
    else:
        score += random.randint(1, 3)

    # Puntuación variable para palabras clave
    palabras_clave = {
        "nuevo": random.randint(1, 2),
        "original": random.randint(1, 2),
        "estado": random.randint(1, 2),
        "colección": random.randint(1, 2),
        "coleccionista": random.randint(1, 2)
    }
    
    score += sum(palabras_clave[palabra] for palabra in palabras_clave if palabra in descripcion.lower())

    return score

def evaluar_precio(precio, categoria):
    precio_medio = sum(precios_referencia[categoria]) / len(precios_referencia[categoria])
    
    # Evaluación más detallada del precio
    diferencia_porcentual = abs(precio - precio_medio) / precio_medio * 100
    
    if diferencia_porcentual < 10:
        return random.randint(1, 2)  # Precio muy cercano
    elif precio < precio_medio:
        return random.randint(2, 3)  # Precio bajo
    else:
        return random.randint(0, 1)  # Precio alto

def calcular_puntaje(producto):
    categoria = "collectibles"
    descripcion_score = evaluar_descripcion(producto["description"])
    precio_score = evaluar_precio(producto["amount"], categoria)

    puntaje_total = descripcion_score + precio_score
    return min(puntaje_total, 10)

def cargar_productos(ruta_archivo):
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
    try:
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        with open(ruta_salida, 'w', encoding='utf-8') as file:
            json.dump(resultados, file, indent=2, ensure_ascii=False)
        print(f"Archivo guardado exitosamente en: {ruta_salida}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

# Ruta del archivo JSON de entrada
ruta_archivo = r'../data/coocked/json/data_coleccionismo.json'

# Ruta del archivo JSON de salida
ruta_salida = r'../data/coocked/json/scoring/data_coleccionismo.json'

# Cargar productos
productos = cargar_productos(ruta_archivo)

# Calcular puntajes para cada producto
resultados = []
if productos:
    for producto in productos:
        puntaje = calcular_puntaje(producto)
        resultados.append({
            "product_id": producto["id"],
            "user_id": producto["user_id"],
            "description": producto["description"],
            "price": f"{producto['amount']} {producto['currency']}",
            "ciudad": producto["ciudad"],
            "taxonomy": producto["taxonomy"],
            "reservado": producto["reservado"],
            "envio": producto["envio"],
            "url_completa": producto["url_completa"],
            "score": puntaje
        })

    # Guardar los resultados en el archivo JSON
    guardar_resultados(resultados, ruta_salida)

    # Imprimir resultados en la consola
    print(json.dumps(resultados, indent=2, ensure_ascii=False))
else:
    print("No se encontraron productos para procesar.")
