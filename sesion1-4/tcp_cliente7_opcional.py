import socket
import sys
import struct

HOST = "localhost"
PUERTO = 9999

if len(sys.argv) > 1:
    HOST = sys.argv[1]
if len(sys.argv) > 2:
    PUERTO = int(sys.argv[2])


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PUERTO))

print(f"Cliente TCP conectado a {HOST}:{PUERTO}")

f = cliente.makefile("rw", encoding="utf8", newline="\n")

# mensaje 1
msg1 = "Hola"
msg1_bytes = msg1.encode("utf8")
cabecera1 = struct.pack("!H", len(msg1_bytes))
cliente.sendall(cabecera1 + msg1_bytes)

# mensaje 2
msg2 = "soy"
msg2_bytes = msg2.encode("utf8")
cabecera2 = struct.pack("!H", len(msg2_bytes))
cliente.sendall(cabecera2 + msg2_bytes)

# mensaje 3
msg3 = "yo."
msg3_bytes = msg3.encode("utf8")
cabecera3 = struct.pack("!H", len(msg3_bytes))
cliente.sendall(cabecera3 + msg3_bytes)

# recepción 1
len1 = struct.unpack("!H", cliente.recv(2))[0]
resp1 = cliente.recv(len1).decode("utf8")
print(repr(resp1))

# recepción 2
len2 = struct.unpack("!H", cliente.recv(2))[0]
resp2 = cliente.recv(len2).decode("utf8")
print(repr(resp2))

# recepción 3
len3 = struct.unpack("!H", cliente.recv(2))[0]
resp3 = cliente.recv(len3).decode("utf8")
print(repr(resp3))

cliente.close()
print("Cliente finalizado.")