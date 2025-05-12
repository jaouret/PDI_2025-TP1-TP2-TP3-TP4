from flask import Flask, render_template_string, request, redirect, url_for
from flask_socketio import SocketIO, emit
import socket
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta'
socketio = SocketIO(app)  # Podés agregar cors_allowed_origins="*" si estás accediendo desde otro dominio

clientes = []
mensajes = []
clientes_lock = threading.Lock()
mensajes_lock = threading.Lock()
apagado = threading.Event()
websocket_activo = threading.Event()

HOST = '127.0.0.1'
PORT = 6667

# ========================
# HTML PLANTILLA
# ========================
template_html = """
<!doctype html>
<html>
<head>
    <title>Servidor TCP con WebSocket</title>
    <script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>
</head>
<body>
    <h2>Servidor TCP</h2>

    <p><b>Clientes conectados:</b></p>
    <ul id="clientes">
        {% for c in clientes %}
            <li>{{ c }}</li>
        {% else %}
            <li>No hay clientes</li>
        {% endfor %}
    </ul>

    <p><b>Mensajes recibidos:</b></p>
    <ul id="mensajes">
        {% for m in mensajes %}
            <li>{{ m }}</li>
        {% else %}
            <li>No hay mensajes</li>
        {% endfor %}
    </ul>

    <form method="post" action="/apagar">
        <button type="submit">Apagar servidor</button>
    </form>

    <form method="post" action="/activar_ws">
        <button type="submit">{{ 'Desactivar' if websocket else 'Activar' }} WebSocket</button>
    </form>

<script>
  const ws_activo = {{ 'true' if websocket else 'false' }};
  if (ws_activo) {
      const socket = io();

      socket.on('connect', function() {
          console.log("[WebSocket] Conectado al servidor");
      });

      socket.on('nuevo_mensaje', function(data) {
          console.log("[WebSocket] Nuevo mensaje:", data);
          var lista = document.getElementById('mensajes');
          var item = document.createElement('li');
          item.textContent = data;
          lista.appendChild(item);
      });

      socket.on('disconnect', function() {
          console.log("[WebSocket] Desconectado");
      });
  }
</script>
</body>
</html>
"""

# ========================
# FLASK ROUTES
# ========================
@app.route('/')
def index():
    with clientes_lock:
        lista_clientes = list(clientes)
    with mensajes_lock:
        lista_mensajes = list(mensajes)
    return render_template_string(template_html, clientes=lista_clientes, mensajes=lista_mensajes, websocket=websocket_activo.is_set())

@app.route('/apagar', methods=['POST'])
def apagar():
    apagado.set()
    print("[SERVIDOR] Apagado solicitado.")
    return redirect(url_for('index'))

@app.route('/activar_ws', methods=['POST'])
def activar_ws():
    if websocket_activo.is_set():
        websocket_activo.clear()
        print("[WebSocket] Desactivado")
    else:
        websocket_activo.set()
        print("[WebSocket] Activado")
    return redirect(url_for('index'))

# ========================
# SOCKET.IO EVENTS
# ========================
def enviar_websocket(mensaje):
    if websocket_activo.is_set():
        print(f"[WebSocket] Enviando: {mensaje}")
        socketio.emit('nuevo_mensaje', mensaje)

# ========================
# SERVIDOR TCP
# ========================
def proceso_hijo(conn, addr):
    ident = f"{addr[0]}:{addr[1]}"
    print(f"[TCP] Nueva conexión desde {ident}")
    with clientes_lock:
        clientes.append(ident)
    try:
        conn.send("Servidor: Conectado con cliente\n".encode('utf-8'))
        while not apagado.is_set():
            data = conn.recv(1024)
            if data:
                mensaje = f"{ident} → {data.decode('utf-8').strip()}"
                print(f"[TCP] {mensaje}")
                with mensajes_lock:
                    mensajes.append(mensaje)
                    if len(mensajes) > 50:
                        mensajes.pop(0)
                enviar_websocket(mensaje)
                conn.sendall(data)
            else:
                break
    except Exception as e:
        import traceback
        print(f"[ERROR] Con {ident}: {e}")
        traceback.print_exc()
    finally:
        conn.close()
        with clientes_lock:
            if ident in clientes:
                clientes.remove(ident)
        print(f"[TCP] Cliente desconectado: {ident}")

def servidor_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    sock.settimeout(1.0)
    print("[SERVIDOR] TCP escuchando en", (HOST, PORT))
    try:
        while not apagado.is_set():
            try:
                conn, addr = sock.accept()
                print(f"[TCP] Cliente aceptado: {addr}")
                threading.Thread(target=proceso_hijo, args=(conn, addr), daemon=True).start()
            except socket.timeout:
                continue
    finally:
        sock.close()
        print("[SERVIDOR] TCP apagado.")

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    threading.Thread(target=servidor_tcp, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
