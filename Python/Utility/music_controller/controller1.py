import tkinter as tk
from tkinter import ttk
import keyboard
import os
import subprocess
from pywinauto import Application

class MusicControllerApp:
    def __init__(self, root):
        self.root = root

        # Configuración de la ventana
        self.root.title("Controlador de Música")
        self.root.attributes("-topmost", True)  # Siempre encima
        self.root.overrideredirect(True)  # Quitar botones estándar
        self.root.geometry("420x50+0+{}".format(self.root.winfo_screenheight() - 50))  # Ajustar tamaño y posición
        self.root.configure(bg="#1e1e1e")  # Fondo oscuro

        # Prevención de desaparición
        self.root.attributes("-disabled", False)
        self.root.attributes("-alpha", 1)  # Asegura que la ventana sea visible en todo momento

        # Deshabilitar clics fuera de la ventana
        self.root.bind("<FocusOut>", self.on_focus_out)

        # Crear controles
        self.create_controls()

        # Atajos de teclado
        keyboard.add_hotkey("altgr+k", self.open_itunes)  # Vincula iTunes al comando AltGr+K
        keyboard.add_hotkey("altgr+m", self.toggle_minimize_window)  # Cambia el atajo para minimizar/restaurar
        keyboard.add_hotkey("altgr+f", self.exit_app)

        # Inicializar iTunes
        self.itunes_app = None

    def create_controls(self):
        """Crea los botones y elementos del controlador."""
        # Frame para botones
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Estilo de botones
        button_styles = {
            "fg": "white", 
            "bg": "#2b2b2b", 
            "font": ("Arial", 10, "bold"),  # Ajustado a 10 para dar más espacio
            "relief": "flat", 
            "activebackground": "#444444", 
            "activeforeground": "white", 
            "width": 3,
            "height": 2
        }

        # Botones del reproductor
        tk.Button(button_frame, text="⏮", command=self.prev_song, **button_styles).pack(side="left", padx=2)
        tk.Button(button_frame, text="⏸", command=self.pause_song, **button_styles).pack(side="left", padx=2)
        tk.Button(button_frame, text="▶️", command=self.play_song, **button_styles).pack(side="left", padx=2)
        tk.Button(button_frame, text="⏭", command=self.next_song, **button_styles).pack(side="left", padx=2)
        tk.Button(button_frame, text="🔄", command=self.toggle_repeat, **button_styles).pack(side="left", padx=2)
        tk.Button(button_frame, text="🔀", command=self.toggle_shuffle, **button_styles).pack(side="left", padx=2)

        # Barra de volumen
        volume_frame = tk.Frame(button_frame, bg="#1e1e1e")
        volume_frame.pack(side="left", fill="y", padx=10)
        
        tk.Label(volume_frame, text="🔉", bg="#1e1e1e", fg="white").pack(side="left", padx=5)
        self.volume = tk.DoubleVar(value=50)
        volume_bar = ttk.Scale(volume_frame, from_=0, to=100, orient="horizontal", variable=self.volume, command=self.set_volume)
        volume_bar.pack(side="left", fill="x", expand=True)

    def prev_song(self):
        if self.itunes_app:
            self.itunes_app.window(title_re=".*iTunes.*").child_window(title="Previous", control_type="Button").click()

    def pause_song(self):
        if self.itunes_app:
            self.itunes_app.window(title_re=".*iTunes.*").child_window(title="Play/Pause", control_type="Button").click()

    def play_song(self):
        if self.itunes_app:
            self.itunes_app.iTunes.PlayPauseButton.click()

    def next_song(self):
        if self.itunes_app:
            self.itunes_app.window(title_re=".*iTunes.*").child_window(title="Next", control_type="Button").click()

    def toggle_repeat(self):
        if self.itunes_app:
            self.itunes_app.window(title_re=".*iTunes.*").child_window(title="Repeat", control_type="Button").click()

    def toggle_shuffle(self):
        if self.itunes_app:
            self.itunes_app.window(title_re=".*iTunes.*").child_window(title="Shuffle", control_type="Button").click()

    def set_volume(self, val):
        if self.itunes_app:
            volume_control = self.itunes_app.window(title_re=".*iTunes.*").child_window(title="Volume", control_type="Slider")
            volume_control.set_focus()
            volume_control.type_keys(int(float(val)))

    def open_itunes(self):
        """Abre iTunes desde la ruta especificada."""
        itunes_path = "C:/Users/rodri/AppData/Local/Microsoft/WindowsApps/AppleInc.iTunes_nzyj5cx40ttqa/iTunes.exe"
        if os.path.exists(itunes_path):
            subprocess.Popen(itunes_path)
            subprocess.Popen(itunes_path, shell=True)
            self.root.after(5000, self.connect_itunes)  # Espera 5 segundos antes de intentar conectar con iTunes
        
    def connect_itunes(self):
        try:
            self.itunes_app = Application(backend="uia").connect(path="iTunes.exe")
        except Exception as e:
            print(f"Error al conectar con iTunes: {e}")
            print("No se pudo encontrar iTunes en la ruta especificada.")

    def toggle_minimize_window(self):
        """Minimiza o restaura la ventana."""
        if self.root.state() == 'withdrawn':
            self.root.deiconify()
        else:
            self.root.withdraw()

    def exit_app(self):
        """Cierra la aplicación."""
        self.root.destroy()

    def on_focus_out(self, _):
        """Mantiene la ventana siempre encima y evita que desaparezca al perder el foco."""
        self.root.attributes("-topmost", True)
        self.root.focus_force()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicControllerApp(root)
    root.mainloop()


#Falta que sea funcional con iTunes y que al hacer click en apps de la barra de tareas 
#no se minimice la ventana