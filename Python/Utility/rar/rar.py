import os
import shutil

def change_extension_to_rar(file_path, new_path):
    file_path = file_path.strip('"').replace('\\', '/')
    new_path = new_path.strip('"').replace('\\', '/')
    
    if not os.path.isfile(file_path):
        print("El archivo no existe.")
        return

    if not file_path.lower().endswith('.rar'):
        base = os.path.splitext(file_path)[0]
        new_file_path = base + '.rar'
        shutil.copy(file_path, new_file_path)
        if not os.path.exists(new_path):
            shutil.move(new_file_path, new_path)
        else:
            print(f"El archivo {new_path} ya existe.")
        print(f"El archivo se ha cambiado a .rar y se ha guardado en {new_path}")
    else:
        print("El archivo ya tiene la extensión .rar")

def main():
    file_path = input("Ingrese la ruta del archivo: ")
    new_path = input("Ingrese la ruta donde desea guardar el archivo con la nueva extensión: ")
    change_extension_to_rar(file_path, new_path)

if __name__ == "__main__":
    main()

#C:/Users/rodri/Downloads
#C:/Users/rodri/Downloads/Examen Práctico Tenis 2023
#C:\Users\rodri\Downloads\Examen Práctico Olimpiadas 2024
#C:/Users/rodri/Downloads/Examen Práctico Tenis 2023 (fichero rar con pdf y csv)
#C:/Users/rodri/Downloads/Examen Práctico Baloncesto 2023 (fichero rar con pdf y csv)