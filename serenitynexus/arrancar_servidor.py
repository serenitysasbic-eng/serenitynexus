import http.server
import socketserver
import webbrowser
import os

# Configuracion simple para computadores veteranos
PORT = 8000

# Esto le dice a Python que use la carpeta actual para mostrar la web
Handler = http.server.SimpleHTTPRequestHandler

print("Iniciando Serenity Nexus Global en tu PC...")
print(f"Abriendo navegador en: http://localhost:{PORT}")

# Este comando abre tu navegador automaticamente
webbrowser.open(f"http://localhost:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Servidor funcionando. (Para apagarlo, cierra esta ventana)")
    httpd.serve_forever()