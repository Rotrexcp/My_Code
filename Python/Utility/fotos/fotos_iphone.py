import os
import shutil
from pathlib import Path

def transfer_files(source_folder, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    
    for root, _, files in os.walk(source_folder):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(destination_folder, os.path.relpath(src_file, source_folder))
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src_file, dest_file)
            print(f"Copiado: {src_file} -> {dest_file}")

def main():
    # Ruta donde se monta el iPhone
    source_folder = "/mnt/iphone/DCIM"  # Cambia esta ruta según tu sistema.
    
    # Ruta del disco duro externo
    destination_folder = "/media/usuario/DiscoDuro/iPhone_Backup"
    
    if not os.path.exists(source_folder):
        print("El iPhone no está montado. Por favor, conéctalo y monta la carpeta.")
        return

    print("Iniciando transferencia...")
    transfer_files(source_folder, destination_folder)
    print("Transferencia completada.")

if __name__ == "__main__":
    main()
