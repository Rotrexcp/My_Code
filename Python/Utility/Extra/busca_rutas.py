import os

def buscar_archivo(nombre_archivo, directorio_base="."):
    for root, _, files in os.walk(directorio_base):
        if nombre_archivo in files:
            ruta = os.path.abspath(os.path.join(root, nombre_archivo))
            return ruta.replace("\\", "/")
    return None

# Ejemplo de uso:
nombre_archivo = input("dime el nombre del archivo: ")  # El nombre del archivo que quieres encontrar
ruta = buscar_archivo(nombre_archivo)

if ruta:
    print(f"Archivo encontrado en: {ruta}")
else:
    print("Archivo no encontrado.")