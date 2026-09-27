import socket
import sys
import uuid
import re

# Valores por defecto
HOST = "localhost"
PUERTO = 9999
contador = 0

# Lectura de argumentos por línea de comandos (IP y Puerto)
if len(sys.argv) > 1:
    HOST = sys.argv[1]
if len(sys.argv) > 2:
    PUERTO = int(sys.argv[2])

# Crear socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect para descartar datagramas que no procedan del servidor
cliente.connect((HOST, PUERTO))

print(f"Cliente UDP listo para enviar a {HOST}:{PUERTO}")
print("Escribe tus mensajes. Envía 'FIN' para terminar.\n")

while True:
    ok = False
    timeout = 0.25
    contador+=1

    # UUID para identificar mensaje y confirmación
    idMensaje = str(uuid.uuid4())

    while timeout <= 2 and not ok:
        linea = input("> ")
        mensaje = f"({idMensaje}){contador}-{linea}"

        # Condición de parada
        if linea == "FIN":
            break

        # Enviar datos codificados en UTF-8
        cliente.send(mensaje.encode("utf-8"))

        cliente.settimeout(timeout)
        try:
            datos = cliente.recv(1024)

            # Extracción del id de la respuesta del servidor para saber a qué mensaje responde
            patronRespuesta = r"^\(([^)]+)\)(.*)"
            match = re.match(patronRespuesta, datos.decode("utf-8"))
            idRespuesta = match.group(1)
            respuesta = match.group(2)

            if idRespuesta==idMensaje and respuesta=="OK":
                print(f"Recibida confirmación del mensaje {idMensaje}")
                ok = True
            else:
                print("Recibido datagrama no esperado")            
        except socket.timeout:
            print("ERROR. El datagrama de confirmación no llega")
            timeout *= 2

    if not ok:
        print("Puede que el servidor esté caído. Inténtelo más tarde")
        break


# Cerrar el socket al salir del bucle
cliente.close()
print("Cliente finalizado.")