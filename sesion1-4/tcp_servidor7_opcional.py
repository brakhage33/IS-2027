import socket
import struct
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

    # f = sd.makefile("rw", encoding="utf8", newline="\n")

    while True:
        # Leer 2 bytes fijos de longitud
        longitud = sd.recv(2)

        if not longitud:
            print("El cliente ha cerrado la conexión")
            sd.close()
            break

        longitud = struct.unpack("!H", longitud)[0]

        mensaje = sd.recv(longitud)
        mensaje = mensaje.decode("utf8")
        print(f"Recibido mensaje ({longitud} bytes): {mensaje}")

        respuesta = mensaje[::-1]
        bytes_respuesta = respuesta.encode("utf8")
        
        longitud_respuesta = len(bytes_respuesta)
        cabecera_respuesta = struct.pack("!H", longitud_respuesta)

        sd.sendall(cabecera_respuesta + bytes_respuesta)
