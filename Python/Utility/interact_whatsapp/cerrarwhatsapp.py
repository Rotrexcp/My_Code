# cerrarwhatsapp.py
import psutil

def funcion_ejecutar():
    # Buscar procesos por nombre
    for proc in psutil.process_iter(['pid', 'name']):
        if 'WhatsApp' in proc.info['name']:  # Cambia esto por el nombre del proceso
            try:
                if proc.is_running():
                    proc.kill()  # Esto fuerza la detención del proceso
                return f"Proceso {proc.info['name']} detenido"
            except psutil.NoSuchProcess:
                return "El proceso ya no existe"
            except psutil.AccessDenied:
                return "Permiso denegado para detener el proceso"
            except Exception as e:
                return f"Error al detener el proceso: {e}"
    return "No se encontró el proceso WhatsApp.exe en ejecución."