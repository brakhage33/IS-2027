import socket
import sys

HOST = "localhost"
PUERTO = 9999

if len(sys.argv) > 1:
    HOST = sys.argv[1]
if len(sys.argv) > 2:
    PUERTO = int(sys.argv[2])


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PUERTO))

print(f"Cliente TCP conectado a {HOST}:{PUERTO}")

for i in range(5):
    cliente.send(b"ABCDE")

cliente.send(b"FINAL")

cliente.close()
print("Cliente finalizado.")
