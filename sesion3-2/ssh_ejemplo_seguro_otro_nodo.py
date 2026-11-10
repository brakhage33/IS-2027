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
key = paramiko.Ed25519Key(data=base64.b64decode(b'AAAAC3NzaC1lZDI1NTE5AAAAILzasBf6MFnFc2VCI8T140+sRorZ4qfP93TTUzvsZQMB'))
client.get_host_keys().add('10.129.184.104', 'ssh-ed25519', key)
client.connect('10.129.184.104', username=usuario, password=contraseña)

print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
