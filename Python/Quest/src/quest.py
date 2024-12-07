# Primera ejecución: bienvenida y lectura de datos

def bienvenida()->tuple:
    saludo = input("Hola muy buenas tardes. Bienvenido a mi Quest, "
                   "para conocerle mejor ingrese su nombre y alguna característica suya (separado por una coma): ")
    nombre, caracteristica = saludo.split(",")
    print(f"Hola {nombre.strip()}, encantado de conocer algo tuyo como: {caracteristica.strip()}")
    return nombre.strip(), caracteristica.strip()

def leer_preguntas(ruta_preguntas: str) -> list:
    with open(ruta_preguntas, encoding="utf-8") as fichero_preguntas:
        return [linea.strip() for linea in fichero_preguntas]

def leer_respuestas(ruta_respuestas: str) -> list:
    with open(ruta_respuestas, encoding="utf-8") as fichero_respuestas:
        return [linea.strip() for linea in fichero_respuestas]

# Segunda ejecución: Tras cambio a Ventana Preguntas
indice_pregunta = 0

def elegir_pregunta(lista_preguntas: list) -> str:
    global indice_pregunta
    if indice_pregunta < len(lista_preguntas):
        pregunta_elegida = lista_preguntas[indice_pregunta]
        indice_pregunta += 1
        return pregunta_elegida
    else:
        return "Se han acabado las preguntas"

def elegir_respuesta(lista_respuestas: list) -> str:
    global indice_pregunta
    if indice_pregunta - 1 < len(lista_respuestas):  # Usamos -1 porque ya incrementamos el índice en la pregunta
        return lista_respuestas[indice_pregunta - 1]
    else:
        return "No hay más respuestas disponibles."

# Función para comparar respuestas
def comparar_respuesta(respuesta_usuario: str, respuesta_correcta: str) -> bool:
    return respuesta_usuario.strip().lower() == respuesta_correcta.strip().lower()

def funcion_principal():
    # Bienvenida al usuario
    bienvenida()

    # Leer preguntas y respuestas
    lista_preguntas = leer_preguntas("./Python/Mis Proyectos/Quest/data/preguntas.txt")
    lista_respuestas = leer_respuestas("./Python/Mis Proyectos/Quest/data/respuestas.txt")

    # Bucle para las preguntas
    for _ in range(min(6, len(lista_preguntas))):  # Hasta 6 preguntas o el máximo disponible
        pregunta = elegir_pregunta(lista_preguntas)
        print(f"Pregunta: {pregunta}")

        respuesta_usuario = input("Tu respuesta: ")
        respuesta_correcta = elegir_respuesta(lista_respuestas)

        if comparar_respuesta(respuesta_usuario, respuesta_correcta):
            print("¡Correcto!")
        else:
            print(f"Incorrecto. La respuesta correcta era: {respuesta_correcta}")

if __name__ == "__main__":
    funcion_principal()
