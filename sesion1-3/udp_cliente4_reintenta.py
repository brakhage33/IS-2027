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
    ok = False
    timeout = 0.25
    contador+=1

    while timeout <= 2 and not ok:
        linea = input("> ")
        mensaje = f"{contador}: {linea}"

        # Condición de parada
        if linea == "FIN":
            break

        # Enviar datos codificados en UTF-8
        cliente.sendto(mensaje.encode("utf-8"), (HOST, PUERTO))

        cliente.settimeout(timeout)
        try:
            datos, direccion = cliente.recvfrom(1024)
            mensaje = datos.decode("utf-8")
            if mensaje=="OK":
                print("Recibida confirmación")
            else:
                print("Recibido datagrama no esperado")
            ok = True
        except socket.timeout:
            print("ERROR. El datagrama de confirmación no llega")
            timeout *= 2

    if not ok:
        print("Puede que el servidor esté caído. Inténtelo más tarde")
        break


# Cerrar el socket al salir del bucle
cliente.close()
print("Cliente finalizado.")