import json

# Funciones para evaluar la calidad de la descripción y el precio
def evaluar_descripcion(descripcion):
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
    if "nuevo" in descripcion.lower() or "en perfecto estado" in descripcion.lower() or "sin estrenar" in descripcion.lower():
        score += 2

    return score

def evaluar_precio(precio):
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

# Leer productos desde un archivo JSON
def cargar_productos(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        return json.load(file)

# Guardar productos procesados en un archivo JSON
def guardar_resultados(resultados, ruta_salida):
    try:
        with open(ruta_salida, 'w', encoding='utf-8') as file:
            json.dump(resultados, file, indent=2, ensure_ascii=False)
        print(f"Archivo guardado exitosamente en: {ruta_salida}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

# Ruta del archivo JSON de entrada
ruta_archivo = '..\\data\\coocked\\json\\data_electrodomesticos.json'  # Cambia esta línea a la ruta de tu archivo JSON

# Ruta del archivo JSON de salida
ruta_salida = '..\\data\\coocked\\json\\scoring\\data_electrodomesticos.json'  # Cambia esta línea a tu ruta de salida

# Cargar productos
productos = cargar_productos(ruta_archivo)

# Calcular puntaje para cada producto
resultados = []
for producto in productos:
    descripcion_score = evaluar_descripcion(producto["description"])
    precio_score = evaluar_precio(producto["amount"])
    puntaje_total = min(descripcion_score + precio_score, 10)  # Limitar el puntaje a un máximo de 10
    
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
        "score": puntaje_total
    })

# Guardar resultados en el archivo especificado
guardar_resultados(resultados, ruta_salida)
