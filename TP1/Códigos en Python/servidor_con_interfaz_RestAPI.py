from flask import Flask, jsonify, render_template, request, redirect, url_for
import time
import threading

app = Flask(__name__)

clientes = []
mensajes = []
clientes_lock = threading.Lock()
mensajes_lock = threading.Lock()
apagado = threading.Event()

# ========================
# FLASK - RUTAS API
# ========================
@app.route('/')
def index():
    with clientes_lock:
        lista_clientes = list(clientes)
    with mensajes_lock:
        lista_mensajes = list(mensajes)
    return render_template("index.html", clientes=lista_clientes, mensajes=lista_mensajes)

@app.route('/mensaje', methods=['POST'])
def recibir_mensaje():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    ip_cliente = request.remote_addr
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with clientes_lock:
        existe = any(c['ip'] == ip_cliente for c in clientes)
        if not existe:
            clientes.append({"ip": ip_cliente, "conexion_time": timestamp})

    with mensajes_lock:
        mensajes.append(f"{timestamp} - {ip_cliente}: {mensaje}")
        if len(mensajes) > 50:
            mensajes.pop(0)

    print(f"[Servidor] {ip_cliente} → {mensaje}")
    return jsonify({"respuesta": f"Mensaje recibido: {mensaje}"}), 200

@app.route('/clientes', methods=['GET'])
def obtener_clientes():
    with clientes_lock:
        return jsonify(clientes)

@app.route('/apagar', methods=['POST'])
def apagar():
    apagado.set()
    return redirect(url_for('index'))

# ========================
# SERVIDOR EN HILO
# ========================
def servidor_loop():
    while not apagado.is_set():
        time.sleep(1)
    print("Servidor apagado.")

# ========================
# MAIN
# ========================
if __name__ == "__main__":
    threading.Thread(target=servidor_loop, daemon=True).start()
    app.run(debug=True, port=5000)

