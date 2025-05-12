import socket

HOST = '127.0.0.1'   # Cambiar esto si el servidor está en otra máquina
PORT = 6667          # Puerto del servidor

try:
    print("Paso 0: Creando socket...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)  # Tiempo máximo de espera para recibir datos

    print(f"Paso 1: Conectando a servidor en {HOST}:{PORT}...")
    sock.connect((HOST, PORT))

    bienvenida = sock.recv(1024)
    print("Paso 2: Mensaje del servidor:", bienvenida.decode('utf-8'))

    print("Paso 3: Listo para ingresar mensaje.")
    mensaje = input("Ingrese un mensaje para enviar al servidor: ")
    sock.sendall(mensaje.encode('utf-8'))
    print("Paso 4: Mensaje enviado, esperando respuesta...")

    try:
        respuesta = sock.recv(1024)
        print("Paso 5: Respuesta del servidor:", respuesta.decode('utf-8'))
    except socket.timeout:
        print("Tiempo de espera agotado. El servidor no respondió.")

except ConnectionRefusedError:
    print("No se pudo conectar al servidor. Verifique si está activo.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    sock.close()
    print("Paso 6: Socket cerrado. Cliente finalizado.")

