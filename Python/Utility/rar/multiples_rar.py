import os
import rarfile
import tkinter as tk
from tkinter import filedialog

def extract_rars(directory):
    for item in os.listdir(directory):
        if item.endswith('.rar'):
            file_path = os.path.join(directory, item)
            with rarfile.RarFile(file_path) as rf:
                rf.extractall(directory)
                print(f'Extracted: {file_path}')

def select_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    return directory

def select_files(directory):
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(initialdir=directory, filetypes=[("RAR files", "*.rar")])
    return file_paths

def main():
    root = tk.Tk()
    root.title("RAR Extractor")
    root.geometry("600x400")  # Ajusta el tamaño de la ventana

    def on_select_directory():
        directory = select_directory()
        if directory:
            rar_files = select_files(directory)
            for file_path in rar_files:
                with rarfile.RarFile(file_path) as rf:
                    rf.extractall(directory)
                    print(f'Extracted: {file_path}')

    select_button = tk.Button(root, text="Select Directory", command=on_select_directory)
    select_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()