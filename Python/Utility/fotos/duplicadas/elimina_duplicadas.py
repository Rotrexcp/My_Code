import os
import hashlib
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def hash_file(file_path):
    """Generate a hash for a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_duplicates(directory):
    """Find and remove duplicate files in a directory."""
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)
            if file_hash in hashes:
                print(f"Duplicate found: {file_path} (duplicate of {hashes[file_hash]})")
                os.remove(file_path)
            else:
                hashes[file_hash] = file_path

def rename_files(directory, text_to_remove):
    """Rename files by removing the specified text and numeric suffixes from their names."""
    for root, _, files in os.walk(directory):
        for file in files:
            new_name = file
            if text_to_remove in file:
                new_name = new_name.replace(text_to_remove, "")
            new_name = re.sub(r'\(\d+\)$', '', new_name)  # Remove numeric suffixes like (1), (2), etc.
            if new_name != file:
                os.rename(os.path.join(root, file), os.path.join(root, new_name))
                print(f"Renamed: {file} to {new_name}")

def open_instructions():
    """Open the instructions file."""
    instructions_path = os.path.join(os.path.dirname(__file__), 'instrucciones.txt')
    os.system(f'notepad.exe {instructions_path}')

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

def run_find_duplicates():
    directory = entry_directory.get()
    if not directory:
        messagebox.showerror("Error", "Por favor, seleccione un directorio.")
        return
    find_duplicates(directory)
    messagebox.showinfo("Completado", "Búsqueda de duplicados completada.")

def run_rename_files():
    directory = entry_directory.get()
    text_to_remove = entry_text_to_remove.get()
    if not directory:
        messagebox.showerror("Error", "Por favor, seleccione un directorio.")
        return
    if not text_to_remove:
        messagebox.showerror("Error", "Por favor, ingrese el texto a eliminar.")
        return
    rename_files(directory, text_to_remove)
    messagebox.showinfo("Completado", "Renombrado de archivos completado.")

root = tk.Tk()
root.title("Elimina Duplicadas y Renombra Archivos")

ICONO_PATH = "C:/Users/rodri/OneDrive/Desktop/US_proyects/Utility/fotos/duplicadas/icono.ico"
root.iconbitmap(ICONO_PATH)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_directory = tk.Label(frame, text="Directorio:")
label_directory.grid(row=0, column=0, sticky="e")

entry_directory = tk.Entry(frame, width=50)
entry_directory.grid(row=0, column=1, padx=5)

button_browse = tk.Button(frame, text="Seleccionar", command=select_directory)
button_browse.grid(row=0, column=2)

button_find_duplicates = tk.Button(frame, text="Buscar Duplicados", command=run_find_duplicates)
button_find_duplicates.grid(row=1, columnspan=3, pady=5)

label_text_to_remove = tk.Label(frame, text="Texto a eliminar:")
label_text_to_remove.grid(row=2, column=0, sticky="e")

entry_text_to_remove = tk.Entry(frame, width=50)
entry_text_to_remove.grid(row=2, column=1, padx=5)

button_rename_files = tk.Button(frame, text="Renombrar Archivos", command=run_rename_files)
button_rename_files.grid(row=3, columnspan=3, pady=5)

button_instructions = tk.Button(frame, text="Instrucciones", command=open_instructions)
button_instructions.grid(row=4, columnspan=3, pady=5)

root.mainloop()
