import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

# Ruta principal de los archivos
RUTA_BASE = "C:/Users/rodri/OneDrive/Desktop/US_proyects/Utility"

# Ruta del ícono personalizado
ICONO_PATH = "C:/Users/rodri/OneDrive/Desktop/US_proyects/Utility/__MANAGER__/manager.ico"

class ManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Manager")
        self.geometry("600x400")
        self.configure(bg="#f4f4f4")  # Fondo claro

        # Establecer ícono de la ventana
        self.iconbitmap(ICONO_PATH)

        # Variables para el historial de navegación
        self.current_path = RUTA_BASE
        self.historial = [RUTA_BASE]
        self.historial_index = 0

        # Etiqueta de bienvenida
        tk.Label(
            self,
            text="Bienvenido al manager de:",
            font=("Arial", 16),
            bg="#f4f4f4",
        ).pack(pady=10)

        tk.Label(
            self,
            text="UTILITY",
            font=("Arial Black", 24),
            bg="#f4f4f4",
            fg="#4CAF50",
        ).pack()

        # Frame donde listaremos los archivos y carpetas
        self.file_frame = ttk.Frame(self)
        self.file_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Botón de salida
        tk.Button(
            self,
            text="SALIR",
            command=self.quit,
            font=("Arial", 12, "bold"),
            bg="#ff4d4d",
            fg="white",
            relief="flat",
            cursor="hand2",
        ).pack(pady=10)

        # Enlazar eventos de mouse para botones 4 (atrás) y 5 (adelante)
        self.bind("<Button-4>", lambda e: self.navegar_atras())
        self.bind("<Button-5>", lambda e: self.navegar_adelante())

        self.cargar_archivos()

    def cargar_archivos(self):
        # Limpiar el frame de archivos
        for widget in self.file_frame.winfo_children():
            widget.destroy()

        try:
            archivos = os.listdir(self.current_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se puede acceder a la ruta: {e}")
            return

        # Listar carpetas primero
        for archivo in sorted(archivos):
            ruta_completa = os.path.join(self.current_path, archivo)
            if os.path.isdir(ruta_completa):
                # Crear botón para la carpeta
                ttk.Button(
                    self.file_frame,
                    text=f"📁 {archivo}",
                    command=lambda r=ruta_completa: self.abrir_carpeta(r),
                ).pack(fill="x", pady=2)

        # Listar archivos después
        for archivo in sorted(archivos):
            ruta_completa = os.path.join(self.current_path, archivo)
            if archivo.endswith(".py") and os.path.isfile(ruta_completa):
                # Crear botón para ejecutar el script
                ttk.Button(
                    self.file_frame,
                    text=f"🐍 {archivo}",
                    command=lambda r=ruta_completa: self.ejecutar_archivo(r),
                ).pack(fill="x", pady=2)
            
            elif archivo.endswith(".txt") and os.path.isfile(ruta_completa):
                ttk.Button(
                    self.file_frame,
                    text=f"📄 {archivo}",
                    command=lambda r=ruta_completa: self.abrir_txt(r),
                ).pack(fill="x", pady=2)

    def abrir_carpeta(self, ruta):
        """
        Abre la carpeta seleccionada.
        """
        self.current_path = ruta
        self.historial = self.historial[: self.historial_index + 1]
        self.historial.append(ruta)
        self.historial_index += 1
        self.cargar_archivos()

    def ejecutar_archivo(self, ruta):
        """
        Ejecuta un archivo Python.
        """
        respuesta = messagebox.askyesno("Ejecutar", f"¿Deseas ejecutar {os.path.basename(ruta)}?")
        if respuesta:
            try:
                subprocess.run(["python", ruta, "--from-manager"], shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo ejecutar el archivo: {e}")
    
    def abrir_txt(self, ruta):
        """
        Abre un archivo .txt con el programa predeterminado del sistema.
        """
        try:
            subprocess.run(["notepad", ruta])  # En Windows, puedes abrir el .txt con el bloc de notas
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo .txt: {e}")

    def navegar_atras(self):
        """
        Navega hacia atrás en el historial.
        """
        if self.historial_index > 0:
            self.historial_index -= 1
            self.current_path = self.historial[self.historial_index]
            self.cargar_archivos()
        else:
            messagebox.showinfo("Información", "No hay más carpetas en el historial hacia atrás.")

    def navegar_adelante(self):
        """
        Navega hacia adelante en el historial.
        """
        if self.historial_index < len(self.historial) - 1:
            self.historial_index += 1
            self.current_path = self.historial[self.historial_index]
            self.cargar_archivos()
        else:
            messagebox.showinfo("Información", "No hay más carpetas en el historial hacia adelante.")


# Ejecutar la aplicación
if __name__ == "__main__":
    app = ManagerApp()
    app.mainloop()
