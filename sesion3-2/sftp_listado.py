import paramiko
import time
import sys
import base64

if (len(sys.argv) != 3):
    print("Error: parámetros erróneos")
    print(f"USO: {sys.argv[0]} <usuario> <contraseña>")
    exit()
usuario = sys.argv[1]
contraseña = sys.argv[2]

client = paramiko.SSHClient()
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAIHEIJr4oJc6oFIdMOn9LEGPdTiEQPQaoVh+jW27W9cP6'))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)
client.connect('localhost', username=usuario, password=contraseña)

print("Conectado!!")

sftp = client.open_sftp()
listado = sftp.listdir()
for nombre in listado:
    print(nombre)

time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
