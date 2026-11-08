#!/usr/bin/env python3
import socket
import sys
import ssl
import getpass

# apartado 1
def RecvReply(sock):
    # recibe socket de hasta un maximo de 1024 bytes y un código (cadena de bytes)
    # imprime por pantalla lo recibido
    reply = sock.recv(1024)
    print("Recibido:", reply.decode(), end='')
    
    # Extrae los tres primeros bytes y los compara con b"+OK"
    if len(reply) < 3 or reply[:3] != b"+OK":
        print(f"ERROR: Se esperaba el código de éxito +OK pero se recibió {reply.decode(errors='ignore')}.")
        sys.exit(1)

# PROGRAMA PRINCIPAL
def main():
    # apartado 2: definir variables server y port
    server = "pop.gmail.com"
    port = 995

    # apartado 3: leer usuario y contraseña
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")

    # apartado 4 : crear la conexión del socket y establecer el canal seguro (puerto 995 usa SSL directo)
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket()
    s.connect((server, port))
    context = ssl.create_default_context()
    sc = context.wrap_socket(s, server_hostname=server)

    # leer el primer mensaje de bienvenida enviado por el servidor
    RecvReply(sc)

    # apartado 5: enviar comando USER
    user_cmd = f"USER {username}\r\n"
    sc.sendall(user_cmd.encode())
    print("\nUSER:")
    RecvReply(sc) # leer respuesta servidor (+OK)

    # apartado 5: enviar comando PASS
    pass_cmd = f"PASS {password}\r\n"
    sc.sendall(pass_cmd.encode())
    print("\nPASS:")
    RecvReply(sc) # leer respuesta servidor (+OK)

    # apartado 6: enviar comando STAT para verificar cuántos correos hay disponibles
    sc.sendall(b"STAT\r\n")
    print("\nSTAT")
    #RecvReply(sc) # correos disponibles en el servidor

    # cambios ej 14:
    reply_stat = sc.recv(1024)
    print("Recibido:", reply_stat.decode(), end='')
    if len(reply_stat) < 3 or reply_stat[:3] != b"+OK":
        sys.exit(1)
    
    partes = reply_stat.decode().split()
    num_mensajes = int(partes[1])
    
    for i in range(1, 5):
        print(f"\n--- CORREO {i} ---")
        retr_cmd = f"RETR {i}\r\n"
        sc.sendall(retr_cmd.encode())
        RecvReply(sc)

        data_correo = b""
        while not data_correo.endswith(b"\r\n.\r\n"):
            chunk = sc.recv(1024)
            if not chunk:
                break
            data_correo += chunk

    # apartado 8: extraer de las cabeceras el campo "Subject" y "From" e imprimirlos
    print("\nCAMPOS SUBJECT Y FROM:")
    for linea in data_correo.split(b"\r\n"):
        linea_str = linea.decode(errors='ignore')
        if linea_str.lower().startswith("from:") or linea_str.lower().startswith("subject:"):
            print(linea_str)

    # Cerrar sesión con QUIT
    sc.sendall(b"QUIT\r\n")
    print("\nQUIT:")
    RecvReply(sc)

    # Cerrar el socket
    s.close()
    print("\n")
    print("Conexión POP3 cerrada con éxito.")

if __name__ == "__main__":
    main()