from flask import Flask, render_template_string, request, redirect, url_for
import socket
import threading
import time

app = Flask(__name__)
clientes = []
mensajes = []
clientes_lock = threading.Lock()
mensajes_lock = threading.Lock()
apagado = threading.Event()

HOST = '127.0.0.1'
PORT = 6667

# ========================
# FLASK - INTERFAZ WEB
# ========================
@app.route('/')
def index():
    with clientes_lock:
        lista_clientes = list(clientes)
    with mensajes_lock:
        log = list(mensajes)
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="3">
        <title>Servidor TCP</title>
    </head>
    <body>
    <h2>Servidor TCP</h2>
    <p><b>Clientes conectados:</b></p>
    <ul>
      {% for c in clientes %}
        <li>{{ c }}</li>
      {% else %}
        <li>No hay clientes conectados</li>
      {% endfor %}
    </ul>
    <p><b>Mensajes recibidos:</b></p>
    <ul>
      {% for m in mensajes %}
        <li>{{ m }}</li>
      {% else %}
        <li>No hay mensajes</li>
      {% endfor %}
    </ul>
    <form method="post" action="/apagar">
        <button type="submit">Apagar servidor</button>
    </form>
    </body>
    </html>
    """, clientes=lista_clientes, mensajes=log)
    
@app.route('/apagar', methods=['POST'])
def apagar():
    apagado.set()
    return redirect(url_for('index'))

# ========================
# SERVIDOR TCP
# ========================
def proceso_hijo(conn, addr):
    with clientes_lock:
        clientes.append(f"{addr[0]}:{addr[1]}")
    try:
        conn.send("Servidor: Conectado con cliente\n".encode('utf-8'))
        while not apagado.is_set():
            data = conn.recv(1024)
            if data:
                mensaje = f"De {addr[0]}:{addr[1]} → {data.decode('utf-8').strip()}"
                print(mensaje)
                with mensajes_lock:
                    mensajes.append(mensaje)
                    if len(mensajes) > 20:
                        mensajes.pop(0)
                conn.sendall(data)
            else:
                break
    except Exception as e:
        print(f"Error con {addr}: {e}")
    finally:
        conn.close()
        with clientes_lock:
            clientes.remove(f"{addr[0]}:{addr[1]}")

def servidor_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    sock.settimeout(1.0)
    print("Servidor TCP escuchando en", (HOST, PORT))
    try:
        while not apagado.is_set():
            try:
                conn, addr = sock.accept()
                threading.Thread(target=proceso_hijo, args=(conn, addr)).start()
            except socket.timeout:
                continue
    finally:
        sock.close()
        print("Servidor apagado.")

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    # Inicia servidor TCP en un hilo
    threading.Thread(target=servidor_tcp, daemon=True).start()

    # Ejecuta la app Flask
    app.run(debug=False, port=5000)
