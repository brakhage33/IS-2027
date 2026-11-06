#!/usr/bin/env python3
import socket
import sys
correo = "uo301086@uniovi.es" # cambiadlo por el vuestro si quereis

def RecvReply(sock, codigo):
    # apartado 1
    # recibe socket de hasta un maximo de 1024 bytes y un código (cadena de bytes)
    # imprime por pantalla lo recibido
    reply = sock.recv(1024)
    print("Recibido:", reply.decode(), end='')
    
    # Extrae los tres primeros bytes y los compara con el código recibido como parámetro
    if len(reply) < 3 or reply[:3] != codigo:
        print(f"ERROR: Se esperaba el código {codigo.decode()} pero se recibió {reply.decode()}.")
        sys.exit(1)

# apartado 2
# PROGRAMA PRINCIPAL
def main():
    server = "relay.uniovi.es"
    port = 25
    fromaddr = correo
    toaddr = correo
    
    subject = "Prueba SMTP crudo"
    data = "Holaaaaa soy un mensaje :)"

    print(f"Conectando a {server}:{port}...")

    # apartado 3: crear una conexión de tipo TCP al servidor usando las variables
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # apartado 4: envía los comandos SMTP necesarios para enviar el correo electrónico
    s.connect((server, port))

    # lama a la función RecvReply para recibir la respuesta y verificar que es correcta (código 220 esperado)
    RecvReply(s, b"220")

    # enviar los comandos SMTP necesarios secuencialmente:
    s.sendall(b"HELO localhost\r\n")
    RecvReply(s, b"250")

    # MAIL FROM
    mail_from_cmd = f"MAIL FROM:<{fromaddr}>\r\n"
    s.sendall(mail_from_cmd.encode())
    RecvReply(s, b"250")

    # RCPT TO
    rcpt_to_cmd = f"RCPT TO:<{toaddr}>\r\n"
    s.sendall(rcpt_to_cmd.encode())
    RecvReply(s, b"250")

    # DATA
    s.sendall(b"DATA\r\n")
    RecvReply(s, b"354")

    # configurar los datos del mensaje
    message = """To: %s
    From: %s
    Subject: %s\r\n\r\n
    %s
    \r\n.\r\n""" % (toaddr, fromaddr, subject, data)
    
    # enviar mensaje
    s.sendall(message.encode())
    RecvReply(s, b"250")

    # QUIT
    s.sendall(b"QUIT\r\n")
    RecvReply(s, b"221")

    # Cerrar el socket TCP
    s.close()
    print("Correo enviado con éxito y conexión cerrada con exito!!")

if __name__ == "__main__":
    main()