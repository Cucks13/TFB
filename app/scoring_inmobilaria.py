import json
import statistics
import os

# Definición de precios de referencia
precios_referencia = {
    "real_estate": [17950, 990, 95, 12900, 50, 1600, 190, 15000, 2200, 1700, 2500, 3000],
    # Aquí se pueden añadir más categorías según sea necesario
}

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

    # Evaluación por palabras clave principales
    palabras_clave_principales = ["nuevo", "artesanal", "calidad", "garantía"]
    if any(keyword in descripcion.lower() for keyword in palabras_clave_principales):
        score += 2

    # Evaluación por palabras clave secundarias
    palabras_clave_secundarias = ["personalizado", "detalles", "características"]
    if any(keyword in descripcion.lower() for keyword in palabras_clave_secundarias):
        score += 1

    return score

def evaluar_precio(precio, categoria):
    try:
        precio_medio = statistics.mean(precios_referencia[categoria])
        if precio < precio_medio:
            return 3  # Precio competitivo
        elif precio == precio_medio:
            return 1  # Precio promedio
        else:
            return 0  # Precio por encima del promedio
    except KeyError:
        return 1  # Valor por defecto si la categoría no existe

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

def procesar_productos(productos):
    resultados = []
    for producto in productos:
        # Asumimos categoría real_estate como predeterminada
        categoria = "real_estate"
        
        descripcion_score = evaluar_descripcion(producto["description"])
        precio_score = evaluar_precio(producto["amount"], categoria)
        puntaje_total = min(descripcion_score + precio_score, 10)
        
        resultados.append({
            "product_id": producto["id"],
            "description": producto["description"],
            "price": f"${producto['amount']}",
            "score": puntaje_total
        })
    return resultados

def main():
    # Ruta del archivo JSON de entrada
    ruta_archivo = '..\data\coocked\json\data_inmobilaria.json'
    
    # Obtener el nombre base del archivo sin extensión y sin ruta
    nombre_base = os.path.basename(ruta_archivo)
    nombre_sin_extension = os.path.splitext(nombre_base)[0]
    
    # Crear el nombre del archivo de salida
    nombre_salida = f"{nombre_sin_extension}.json"
    
    # Crear la ruta completa de salida
    ruta_salida = os.path.join('..', 'data', 'coocked', 'json', 'scoring', nombre_salida)
    
    # Asegurar que el directorio de salida existe
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    # Cargar productos
    productos = cargar_productos(ruta_archivo)
    
    if productos:
        # Procesar productos y obtener resultados
        resultados = procesar_productos(productos)
        
        # Generar salida en formato JSON
        output_json = json.dumps(resultados, indent=2, ensure_ascii=False)
        print(output_json)
        
        # Guardar resultados en el archivo
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        print(f"Archivo guardado exitosamente en: {ruta_salida}")

if __name__ == "__main__":
    main()