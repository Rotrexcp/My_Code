from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def home():
    # HTML con un script para forzar la descarga
    return """
    <html>
    <head>
        <title>Descarga automática</title>
    </head>
    <body>
        <h1>¡Tu archivo se está descargando automáticamente!</h1>
        <p>Si estás usando Safari, asegúrate de permitir descargas automáticas en la configuración del navegador.</p>
        <script>
            window.onload = function() {
                window.location.href = "/descargar";
            };
        </script>
    </body>
    </html>
    """

@app.route("/descargar")
def descargar():
    # Descargar el archivo automáticamente
    return send_file("perrito.jpeg", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")