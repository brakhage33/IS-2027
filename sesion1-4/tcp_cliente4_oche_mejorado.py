import socket
import sys

def recibe_mensaje(socket):
    buffer = []
    term = [b"\r", b"\n"]
    while True:
        buffer.append(socket.recv(1))
        if (buffer[-1::] == [b""]):
            return b""
        if (buffer[-2::] == term):
            return b"".join(buffer)

HOST = "localhost"
PUERTO = 9999

if len(sys.argv) > 1:
    HOST = sys.argv[1]
if len(sys.argv) > 2:
    PUERTO = int(sys.argv[2])


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PUERTO))

print(f"Cliente TCP conectado a {HOST}:{PUERTO}")

cliente.sendall(bytes("Hola\r\n", "utf8"))
cliente.sendall(bytes("soy\r\n", "utf8"))
cliente.sendall(bytes("yo.\r\n", "utf8"))

print(repr(recibe_mensaje(cliente)))
print(repr(recibe_mensaje(cliente)))
print(repr(recibe_mensaje(cliente)))



cliente.sendall(bytes("", "utf8"))

cliente.close()
print("Cliente finalizado.")
