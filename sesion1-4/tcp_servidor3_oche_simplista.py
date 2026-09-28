import socket
import sys
import time

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
    #time.sleep(1)
    print("Nuevo cliente conectado desde %s, %d" % origen)

    while True:
        # Primero recibir el mensaje del cliente
        mensaje = sd.recv(80)  # Nunca enviará más de 80 bytes, aunque tal vez sí menos
        mensaje = str(mensaje, "utf8") # Convertir los bytes a caracteres

        if mensaje == "":
            print("El cliente ha cerrado la conexión")
            sd.close()
            break
        else:
            print("Recibido mensaje: %s" % mensaje)

        # Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
        linea = mensaje[:-2]  # slice desde el principio hasta el final -2

        # Tercero, darle la vuelta
        linea = linea[::-1]

        # Finalmente, enviarle la respuesta con un fin de línea añadido
        # Observa la transformación en bytes para enviarlo
        sd.sendall(bytes(linea+"\r\n", "utf8"))
