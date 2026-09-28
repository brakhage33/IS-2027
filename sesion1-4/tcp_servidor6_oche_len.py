import socket
import sys
import time

PUERTO = 9999

if len(sys.argv) > 1:
    PUERTO = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("", PUERTO))
s.listen(5)

print(f"Servidor TCP escuchando en el puerto {PUERTO}...")


while True:
    print("Esperando un cliente")
    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)

    f = sd.makefile("rw", encoding="utf8", newline="\n")

    while True:
        # Primero leer la longitud del mensaje
        longitud = f.readline()

        if longitud == "":
            print("El cliente ha cerrado la conexión")
            sd.close()
            break

        longitud = int(longitud.strip())

        mensaje = f.read(longitud)
        print(f"Recibido mensaje ({longitud} bytes): {mensaje}")

        respuesta = mensaje[::-1]

        bytes_respuesta = bytes(respuesta, "utf8")
        longitud_respuesta = len(bytes_respuesta)

        f.write(f"{longitud_respuesta}\n{respuesta}")
        f.flush()
