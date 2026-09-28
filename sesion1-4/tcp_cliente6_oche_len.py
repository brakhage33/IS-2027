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

f = cliente.makefile("rw", encoding="utf8", newline="\n")

# mensaje 1
msg1 = "Hola"
f.write(f"{len(bytes(msg1, 'utf8'))}\n{msg1}")
f.flush()

# mensaje 2
msg2 = "soy"
f.write(f"{len(bytes(msg2, 'utf8'))}\n{msg2}")
f.flush()

# mensaje 3
msg3 = "yo."
f.write(f"{len(bytes(msg3, 'utf8'))}\n{msg3}")
f.flush()

# recepción 1
len1 = int(f.readline().strip())
resp1 = f.read(len1)
print(repr(resp1))

# recepción 2
len2 = int(f.readline().strip())
resp2 = f.read(len2)
print(repr(resp2))

# recepción 3
len3 = int(f.readline().strip())
resp3 = f.read(len3)
print(repr(resp3))

cliente.close()
print("Cliente finalizado.")
