import paramiko
import time
import sys

if (len(sys.argv) != 3):
    print("Error: parámetros erróneos")
    print(f"USO: {sys.argv[0]} <usuario> <contraseña>")
    exit()
usuario = sys.argv[1]
contraseña = sys.argv[2]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())
client.connect('localhost', username=usuario, password=contraseña)
print("Conectado!!")

# Ejecutar comando remoto, redireccionando sus salidas
stdin, stdout, stderr = client.exec_command('ls')

# Mostrar resultado de la ejecución (rstrip quita los retornos de carro)
for line in stdout:
    print(line.rstrip())
time.sleep(1)  # Dar tiempo a que se vacie el buffer
client.close()
