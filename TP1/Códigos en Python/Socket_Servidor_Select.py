# Socket_Servidor_Select.py
# Servidor con Select()

import select
import socket
import sys
import queue

# Creando un socket TCP/IP 
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setblocking(0)

# Hago Bind del socket al puerto
dir_servidor = ('localhost', 10000)
print('iniciando en {} port {}'.format(*dir_servidor),
      file=sys.stderr)
servidor.bind(dir_servidor)

# Escucho conexiones entrantes
servidor.listen(5)

# Sockect que espero leer
entradas = [servidor]

# Sockets que espero enviar
salidas = []

# Cola de mensajes salientes
cola_mensajes = {}

while entradas:

    # Espero a que al menos uno de los sockets este listo para ser procesado
    
    print('esperando el próximo evento', file=sys.stderr)
    readable, writable, exceptional = select.select(entradas,
                                                    salidas,
                                                    entradas)

    if not (readable or writable or exceptional):
        print('  tiempo excedido....',
              file=sys.stderr)
        continue
    # Manejo entradas
    for s in readable:

        if s is servidor:
            # Un socket "leíble" está listo para aceptar conexiones
            con, dir_cliente = s.accept()
            print('  conexión desde: ', dir_cliente,
                  file=sys.stderr)
            con.setblocking(0)
            entradas.append(con)

            # Le asigno a la conexión una cola en la cuál quiero enviar
            cola_mensajes[con] = queue.Queue()

        else:
            data = s.recv(1024)
            if data:
                # Un socket leíble tiene datos
                print('  recibido {!r} desde {}'.format(
                    data, s.getpeername()), file=sys.stderr,
                )
                cola_mensajes[s].put(data)
                # Agrego un canal de salida para la respuesta
                if s not in salidas:
                    salidas.append(s)
            else:
                # Si está vacío lo interpreto como una conexión a cerrar
                print('  cerrando...', dir_cliente,
                      file=sys.stderr)
                # dejo de escuchar en la conexión
                if s in salidas:
                    salidas.remove(s)
                entradas.remove(s)
                s.close()

                # Rremueve mensaje de la cola
                del cola_mensajes[s]
    # Administro salidas
    for s in writable:
        try:
            next_msg = cola_mensajes[s].get_nowait()
        except queue.Empty:
            # No hay mensaje en espera. Dejo de controlar para posibles escrituras
            
            print('  ', s.getpeername(), 'cola vacía',
                  file=sys.stderr)
            salidas.remove(s)
        else:
            print(' enviando {!r} a {}'.format(next_msg, s.getpeername()), file=sys.stderr)
            s.send(next_msg)

  # Administro condiciones excepcionales"
    for s in exceptional:
        print('excepción en', s.getpeername(),
              file=sys.stderr)
        # Dejo de escuchar en las conexiones
        entradas.remove(s)
        if s in salidas:
            salidas.remove(s)
        s.close()

        # Remuevo cola de mensajes
        del cola_mensajes[s]
