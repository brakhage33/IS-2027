import socket
import sys

PUERTO = 12345

IP_BROADCAST = "255.255.255.255"

if len(sys.argv) > 1:
    IP_BROADCAST = sys.argv[1]
if len(sys.argv) > 2:
    PUERTO = int(sys.argv[2])


cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

mensaje = "BUSCANDO HOLA"
cliente.sendto(mensaje.encode("utf-8"), (IP_BROADCAST, PUERTO))
print(f"Enviado '{mensaje}' a {IP_BROADCAST}:{PUERTO}")

cliente.settimeout(2)
servidores = []

while True:
    try:
        datos, origen = cliente.recvfrom(1024)
        respuesta = datos.decode("utf-8")

        if respuesta == "IMPLEMENTO HOLA":
            ip_servidor = origen[0]
            print(f"Servidor encontrado en {ip_servidor}")
            servidores.append(ip_servidor)
    except socket.timeout:
        # No llegan más respuestas: asumimos que ya respondieron todos
        break

if servidores:
    servidor_elegido = servidores[0]
    print(f"\nProbando el servicio con el servidor {servidor_elegido}...")

    cliente.sendto("HOLA".encode("utf-8"), (servidor_elegido, PUERTO))

    datos, origen = cliente.recvfrom(1024)
    respuesta = datos.decode("utf-8")
    print(f"Respuesta recibida: {respuesta}")
else:
    print("No se ha encontrado ningún servidor.")

cliente.close()
