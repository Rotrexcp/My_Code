import os
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Ruta del archivo de configuración
CONFIG_FILE = "C:/Users/rodri/OneDrive/Desktop/My_Code/Python/Utility/PDF/pdf_sets.json"
ICON_PATH = "C:/Users/rodri/OneDrive/Desktop/My_Code/Python/Utility/PDF/multiplePDF.ico"

def load_sets():
    """Carga los conjuntos de PDFs desde un archivo JSON."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}

def save_sets(pdf_sets):
    """Guarda los conjuntos de PDFs en un archivo JSON."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(pdf_sets, file, indent=4)

def add_set(pdf_sets, name, file_paths):
    """Añade un nuevo conjunto al diccionario de conjuntos."""
    if name in pdf_sets:
        messagebox.showerror("Error", f"El conjunto '{name}' ya existe.")
        return False
    pdf_sets[name] = file_paths
    save_sets(pdf_sets)
    return True

def replace_set(pdf_sets, name, new_file_paths):
    """Reemplaza un conjunto existente en el diccionario de conjuntos."""
    if name not in pdf_sets:
        messagebox.showerror("Error", f"El conjunto '{name}' no existe.")
        return False
    pdf_sets[name] = new_file_paths
    save_sets(pdf_sets)
    return True

def append_to_set(pdf_sets, name, new_file_paths):
    """Agrega archivos a un conjunto existente en el diccionario de conjuntos."""
    if name not in pdf_sets:
        messagebox.showerror("Error", f"El conjunto '{name}' no existe.")
        return False
    pdf_sets[name].extend(new_file_paths)
    save_sets(pdf_sets)
    return True

def delete_set(pdf_sets, name):
    """Elimina un conjunto del diccionario de conjuntos."""
    if name in pdf_sets:
        del pdf_sets[name]
        save_sets(pdf_sets)
        return True
    messagebox.showerror("Error", f"El conjunto '{name}' no existe.")
    return False

def open_set(file_paths):
    """Abre todos los PDFs de un conjunto con Adobe Acrobat."""
    for file_path in file_paths:
        if os.path.exists(file_path):
            subprocess.Popen(["start", "", file_path], shell=True)
        else:
            messagebox.showwarning("Advertencia", f"El archivo no existe: {file_path}")

# Funciones de la interfaz gráfica
def create_set_ui(pdf_sets, listbox):
    """Abre un diálogo para crear un nuevo conjunto."""
    name = simpledialog.askstring("Nombre del conjunto", "Introduce el nombre del conjunto:")
    if not name:
        return

    file_paths = filedialog.askopenfilenames(
        title="Selecciona PDFs",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not file_paths:
        return

    if add_set(pdf_sets, name, file_paths):
        listbox.insert(tk.END, f"{name} ({len(file_paths)} PDFs)")

def replace_set_ui(pdf_sets, listbox):
    """Abre un diálogo para reemplazar el conjunto seleccionado."""
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Información", "Selecciona un conjunto primero.")
        return

    name = listbox.get(selected[0]).split(" (")[0]
    new_file_paths = filedialog.askopenfilenames(
        title="Selecciona PDFs para reemplazar el conjunto",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not new_file_paths:
        return

    if replace_set(pdf_sets, name, new_file_paths):
        listbox.delete(selected[0])
        listbox.insert(selected[0], f"{name} ({len(new_file_paths)} PDFs)")

def append_set_ui(pdf_sets, listbox):
    """Abre un diálogo para agregar archivos al conjunto seleccionado."""
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Información", "Selecciona un conjunto primero.")
        return

    name = listbox.get(selected[0]).split(" (")[0]
    new_file_paths = filedialog.askopenfilenames(
        title="Selecciona PDFs para agregar al conjunto",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not new_file_paths:
        return

    # Combina los archivos nuevos con los existentes en el conjunto
    if name in pdf_sets:
        current_files = pdf_sets[name]
        pdf_sets[name] = list(set(list(current_files) + list(new_file_paths)))  # Convierte current_files a lista
        save_sets(pdf_sets)

        # Actualiza la lista visual con el nuevo conteo de archivos
        listbox.delete(selected[0])
        listbox.insert(selected[0], f"{name} ({len(pdf_sets[name])} PDFs)")

        messagebox.showinfo("Éxito",f"El conjunto '{name}' ha sido editado.")
    else:
        messagebox.showerror("Error", f"El conjunto '{name}' no existe.")

def delete_set_ui(pdf_sets, listbox):
    """Elimina el conjunto seleccionado."""
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Información", "Selecciona un conjunto primero.")
        return

    name = listbox.get(selected[0]).split(" (")[0]
    if messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar el conjunto '{name}'?"):
        if delete_set(pdf_sets, name):
            listbox.delete(selected[0])

def open_selected_set(pdf_sets, listbox):
    """Abre el conjunto seleccionado en la lista."""
    selected = listbox.curselection()
    if not selected:
        messagebox.showinfo("Información", "Selecciona un conjunto primero.")
        return

    set_name = listbox.get(selected[0]).split(" (")[0]
    if set_name in pdf_sets:
        open_set(pdf_sets[set_name])
    else:
        messagebox.showerror("Error", f"No se encontró el conjunto: {set_name}")

def main():
    """Función principal para la interfaz gráfica."""
    pdf_sets = load_sets()

    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Gestor de Conjuntos de PDFs")
    root.geometry("450x450")
    root.iconbitmap(ICON_PATH)

    # Lista de conjuntos
    listbox = tk.Listbox(root, width=50, height=20)
    listbox.pack(pady=10)

    for name, files in pdf_sets.items():
        listbox.insert(tk.END, f"{name} ({len(files)} PDFs)")

    # Botones
    frame = tk.Frame(root)
    frame.pack()

    btn_create = tk.Button(frame, text="Crear", command=lambda: create_set_ui(pdf_sets, listbox))
    btn_create.grid(row=0, column=0, padx=5)

    btn_open = tk.Button(frame, text="Abrir", command=lambda: open_selected_set(pdf_sets, listbox))
    btn_open.grid(row=0, column=1, padx=5)

    btn_append = tk.Button(frame, text="Editar", command=lambda: append_set_ui(pdf_sets, listbox))
    btn_append.grid(row=0, column=2, padx=5)

    btn_replace = tk.Button(frame, text="Reemplazar", command=lambda: replace_set_ui(pdf_sets, listbox))
    btn_replace.grid(row=0, column=3, padx=5)

    btn_delete = tk.Button(frame, text="Eliminar", command=lambda: delete_set_ui(pdf_sets, listbox))
    btn_delete.grid(row=0, column=4, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()
