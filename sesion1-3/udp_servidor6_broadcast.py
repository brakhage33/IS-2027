import socket
import sys

PUERTO = 12345

if len(sys.argv) > 1:
    PUERTO = int(sys.argv[1])

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

servidor.bind(("", PUERTO))

print(f"Servidor HOLA escuchando en el puerto {PUERTO}...")

while True:
    datos, direccion = servidor.recvfrom(1024)
    mensaje = datos.decode("utf-8")

    print(f"Datagrama recibido de {direccion}: {mensaje}")

    if mensaje == "BUSCANDO HOLA":
        respuesta = "IMPLEMENTO HOLA"
        servidor.sendto(respuesta.encode("utf-8"), direccion)

    elif mensaje == "HOLA":
        ip_cliente = direccion[0]
        respuesta = f"HOLA: {ip_cliente}"
        servidor.sendto(respuesta.encode("utf-8"), direccion)
