# Socket_Servidor_Concurrente_01.py
# servidor concurrente con opción de apagado

import socket
import threading
import time

host = "127.0.0.1"
port = 6667

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
print("Socket bind completado")
sock.listen(5)
print("Socket en modo escucha - pasivo")

clientes = []
apagado = threading.Event()

def proceso_hijo(conn, addr):
    print('Conexión con {}.'.format(addr))
    clientes.append(conn)
    try:
        conn.send("Servidor: Conectado con cliente\n".encode('utf-8'))

        while not apagado.is_set():
            data = conn.recv(10)
            if data:
                print('Recibido de {}: {}'.format(addr, data.decode('utf-8')))
                conn.sendall(data)
            else:
                print('No hay más datos de', addr)
                break
    except Exception as e:
        print("Error con {}: {}".format(addr, e))
    finally:
        conn.close()
        clientes.remove(conn)

def control_apagado():
    while not apagado.is_set():
        time.sleep(30)
        respuesta = input("\n¿Desea apagar el servidor? (s/n): ").strip().lower()
        if respuesta == 's':
            apagado.set()
            print("Apagando servidor...")
            break

# Iniciar el hilo de control
threading.Thread(target=control_apagado, daemon=True).start()

# Aceptar conexiones mientras no se apague
try:
    while not apagado.is_set():
        sock.settimeout(1.0)
        try:
            conn, addr = sock.accept()
            threading.Thread(target=proceso_hijo, args=(conn, addr)).start()
        except socket.timeout:
            continue
finally:
    print("Cerrando todas las conexiones...")
    for c in clientes:
        c.close()
    sock.close()
    print("Servidor finalizado.")
