import json
import os

# Definición de precios de referencia
precios_referencia = {
    "home_garden": [25.0, 100.0, 45.0, 140.0, 70.0, 125.0, 50.0, 15.0, 150.0, 10.0, 13.0, 90.0, 220.0, 50.0, 120.0, 150.0, 4.0, 600.0, 45.0, 35.0, 190.0, 4.99, 100.0],
    # ... (otros precios de referencia)
}

# Función para evaluar la descripción
def evaluar_descripcion(descripcion):
    score = 0
    if len(descripcion) > 150:
        score += 5
    elif len(descripcion) > 100:
        score += 4
    elif len(descripcion) > 50:
        score += 3
    else:
        score += 1

    if any(keyword in descripcion.lower() for keyword in ["nuevo", "artesanal", "perfecto", "calidad"]):
        score += 2
    if any(keyword in descripcion.lower() for keyword in ["garantía", "personalizado", "decora"]):
        score += 1

    return score

# Función para evaluar el precio
def evaluar_precio(precio, categoria):
    precio_medio = sum(precios_referencia[categoria]) / len(precios_referencia[categoria])
    if precio < precio_medio:
        return 3  # Bajo precio
    elif precio == precio_medio:
        return 1  # Precio promedio
    else:
        return 0  # Precio alto

# Función para calcular el puntaje total
def calcular_puntaje(producto):
    categoria = "home_garden"  # Asumimos que todos son del hogar y jardín
    descripcion_score = evaluar_descripcion(producto["description"])
    precio_score = evaluar_precio(producto["amount"], categoria)

    puntaje_total = descripcion_score + precio_score
    return min(puntaje_total, 10)

# Función para guardar resultados en un archivo JSON
def guardar_resultados(resultados, ruta_salida):
    try:
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        with open(ruta_salida, 'w', encoding='utf-8') as file:
            json.dump(resultados, file, indent=2, ensure_ascii=False)
        print(f"Archivo guardado exitosamente en: {ruta_salida}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

# Ruta del archivo JSON de entrada
ruta_archivo = '..\\data\\coocked\\json\\data_hogar_jardin.json'  # Cambia esta línea a la ruta de tu archivo JSON

# Ruta del archivo JSON de salida
ruta_salida = '..\\data\\coocked\\json\\scoring\\data_hogar_jardin.json'  # Cambia esta línea a tu ruta de salida

# Leer productos desde un archivo JSON
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

# Procesar productos
productos = cargar_productos(ruta_archivo)

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

    # Guardar los resultados en un archivo JSON
    guardar_resultados(resultados, ruta_salida)
else:
    print("No se encontraron productos para procesar.")
