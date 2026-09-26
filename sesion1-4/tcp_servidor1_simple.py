import socket
import sys


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
    continuar = True

    while continuar:
        datos = sd.recv(5)
        datos = datos.decode("ascii")

        if datos == "":
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False
        elif datos == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False
        else:
            print("Recibido mensaje: %s" % datos)
