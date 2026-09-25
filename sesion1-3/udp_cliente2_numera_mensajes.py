import socket
import sys

# Valores por defecto
HOST = "localhost"
PUERTO = 9999
contador = 0

# Lectura de argumentos por línea de comandos (IP y Puerto)
if len(sys.argv) > 1:
    HOST = sys.argv[1]
if len(sys.argv) > 2:
    PUERTO = int(sys.argv[2])

# Crear socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Cliente UDP listo para enviar a {HOST}:{PUERTO}")
print("Escribe tus mensajes. Envía 'FIN' para terminar.\n")

while True:
    linea = input("> ")
    mensaje = f"{contador}-{linea}"
    contador+=1

    # Condición de parada
    if linea == "FIN":
        break
    
    # Enviar datos codificados en UTF-8
    cliente.sendto(mensaje.encode("utf-8"), (HOST, PUERTO))

# Cerrar el socket al salir del bucle
cliente.close()
print("Cliente finalizado.")