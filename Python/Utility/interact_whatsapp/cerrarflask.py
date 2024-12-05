# app.py
from flask import Flask, redirect, url_for
import cerrarwhatsapp  # Importamos el archivo cerrarwhatsapp.py

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('ejecutar_funcion'))  # Redirige automáticamente a /ejecutar

@app.route('/ejecutar')
def ejecutar_funcion():
    resultado = cerrarwhatsapp.funcion_ejecutar()  # Llamamos a la función del otro archivo
    return f'<h1>{resultado}</h1>'

if __name__ == '__main__':
    # Cambiar '0.0.0.0' por tu IP local si prefieres especificarla directamente
    app.run(host='0.0.0.0', port=5000, debug=True)