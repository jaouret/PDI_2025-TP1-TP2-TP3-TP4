#!/usr/bin/python
# Socket_Cliente_Connect_01C.py
import socket
import sys
import time

# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket en el puerto cuando el servidor esté escuchando
server_dir = ('localhost', 6667)
print('conectando a %s puerto %s' % server_dir)
sock.connect(server_dir)

contador = 0
while contador < 10:  # Cambié <=10 a <10 para que sean 10 mensajes
    # Enviando datos
    print("Paso:", contador)
    mensaje = b'123456789'
    print('Enviando mensaje "%s"' % mensaje)
    sock.sendall(mensaje)

    # Esperando la respuesta del servidor
    data = sock.recv(1024)  # Leemos hasta 1024 bytes
    if data:
        print('Recibiendo mensaje "%s"' % data.decode('utf-8'))
    else:
        print("El servidor cerró la conexión.")
        break  # Si no recibimos datos, terminamos
    
    # Pausa de 2 segundos entre cada mensaje
    time.sleep(2)  # Retraso de 1 segundo entre envíos de mensajes

    contador += 1
    print("Paso:", contador)

print('cerrando socket')
sock.close()
sys.exit(0)  # Terminar el programa
