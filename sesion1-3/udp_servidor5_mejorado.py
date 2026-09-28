import socket
import sys
import random
import re

# Puerto por defecto
PUERTO = 9999

# Si se pasa un puerto por línea de comandos, lo usamos
if len(sys.argv) > 1:
    puerto = int(sys.argv[1])
else:
    puerto = PUERTO

# Crear socket UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

servidor.bind(("", puerto))

print(f"Servidor UDP escuchando en el puerto {puerto}...")

while True:
    datos, direccion = servidor.recvfrom(1024)

    # Pérdida aleatoria de datagramas
    if random.randint(0, 1) == 0:
        print("Simulando paquete perdido")
    else:
        # Extracción del UUID del mensaje para confirmación
        patronMensaje = r"^\(([^)]+)\)(.*)"
        match = re.match(patronMensaje, datos.decode("utf-8"))
        idMensaje = match.group(1)
        mensaje = match.group(2)
        print(f"Mensaje recibido de {direccion}: ({idMensaje}){mensaje}")

        # Confirmación con UUID 
        confirmacion = f"({idMensaje})OK"

        # Envío de mensaje de confirmación
        servidor.sendto(confirmacion.encode("utf-8"), direccion)
