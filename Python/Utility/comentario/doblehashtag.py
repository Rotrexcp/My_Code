import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

OUTPUT_FILE = "C:/Users/rodri/OneDrive/Desktop/US_proyects/Utility/comentario/important_comments.txt"

class CommentLogger(FileSystemEventHandler):
    def __init__(self, folder_to_monitor):
        self.folder_to_monitor = folder_to_monitor

    def process_file(self, file_path):
        if not file_path.endswith('.py'):  # Solo procesa archivos Python
            return

        file_name = os.path.basename(file_path)  # Extraer solo el nombre del archivo

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Buscar comentarios importantes
        important_comments = [
            (idx + 1, line.strip()) for idx, line in enumerate(lines) if line.strip().startswith("##")
        ]

        if important_comments:
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as output_file:
                for line_number, comment in important_comments:
                    # Registrar comentarios con información del archivo y la línea
                    output_file.write(
                        f"[{file_name}:L{line_number}] {comment}\n"
                    )
            print(f"Comentarios importantes añadidos desde: {file_name}")

    def on_modified(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

def start_monitoring(folder_to_monitor):
    print(f"Monitoreando cambios en: {folder_to_monitor}")
    event_handler = CommentLogger(folder_to_monitor)
    observer = Observer()
    observer.schedule(event_handler, folder_to_monitor, recursive=True)
    observer.start()

    try:
        while True:
            pass  # Mantener el programa corriendo
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_monitor = os.getcwd()  # Monitorea el directorio actual
    start_monitoring(folder_to_monitor)
