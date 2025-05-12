# Cliente usando requests para comunicarse con Flask (simulando el envío de mensajes 10 veces)
#!/usr/bin/python
# cliente_restapi.py

import requests
import time
import sys

# Dirección del servidor Flask
URL = "http://localhost:5000"

contador = 0
while contador < 10:
    print(f"Paso: {contador}")

    # Simulamos un mensaje que el cliente quiere enviar al servidor
    mensaje = f"Mensaje {contador}"
    print(f"Enviando mensaje: {mensaje}")

    try:
        # Enviar el mensaje al servidor a través de una solicitud POST
        response = requests.post(f"{URL}/mensaje", json={"mensaje": mensaje})
        if response.status_code == 200:
            print("Respuesta del servidor:", response.json().get("respuesta"))
        else:
            print("Error del servidor:", response.status_code)
    except Exception as e:
        print("Error en la conexión:", e)
        break

    time.sleep(2)  # Esperar 2 segundos
    contador += 1

print("Finalizando cliente.")
sys.exit(0)
