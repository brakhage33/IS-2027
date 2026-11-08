#!/usr/bin/env python3
import socket
import sys
import email.message, email.policy, email.utils
import time
import ssl
import base64
import getpass

correo = "emma.sanchez.couso@gmail.com" # cambiadlo por el vuestro si quereis

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
    server = "smtp.gmail.com"
    port = 587
    fromaddr = "correofalso@mentira.com"
    toaddr = "uo301086@uniovi.es"

    print(f"Conectando a {server}:{port}...")

    # apartado 3: crear una conexión de tipo TCP al servidor usando las variables
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # apartado 4: envía los comandos SMTP necesarios para enviar el correo electrónico
    s.connect((server, port))

    # lama a la función RecvReply para recibir la respuesta y verificar que es correcta (código 220 esperado)
    RecvReply(s, b"220")

    # enviar los comandos SMTP necesarios secuencialmente:
    s.sendall(b"EHLO localhost\r\n")
    RecvReply(s, b"250")
    
    # STARTTLS
    s.sendall(b"STARTTLS\r\n")
    RecvReply(s, b"220")
    
    # envolver socket en TLS con wrap socket
    context = ssl.create_default_context()
    sc = context.wrap_socket(s, server_hostname=server)
    # wrap_socket cifra el canal, entonces a partir de ahora enviamos comandos por sc
 
    # Por protocolo, tras iniciar TLS hay que volver a saludar con EHLO por el canal seguro:
    sc.sendall(b"EHLO localhost\r\n")
    RecvReply(sc, b"250")
    
    # AUTH LOGIN
    sc.sendall(b"AUTH LOGIN\r\n")
    RecvReply(sc, b"334")
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")

    sc.send(base64.b64encode(username.encode("ascii"))+b'\r\n')
    # Leer respuesta (esperamos 334)
    RecvReply(sc, b"334")

    sc.send(base64.b64encode(password.encode("utf8"))+b'\r\n')
    # Leer respuesta (esperamos 235)
    RecvReply(sc, b"235")

    # MAIL FROM
    mail_from_cmd = f"MAIL FROM:<{fromaddr}>\r\n"
    sc.sendall(mail_from_cmd.encode())
    RecvReply(sc, b"250")

    # RCPT TO
    rcpt_to_cmd = f"RCPT TO:<{toaddr}>\r\n"
    sc.sendall(rcpt_to_cmd.encode())
    RecvReply(sc, b"250")

    # DATA
    sc.sendall(b"DATA\r\n")
    RecvReply(sc, b"354")

    # configurar los datos del mensaje
    mensaje = email.message.EmailMessage()
    mensaje['To'] = 'Desti Natario <destinatario@example.com>'
    mensaje['From'] = 'Remi Tente <remitente@example.com>'
    mensaje['Subject'] = 'Mensaje de prueba'
    mensaje['Date'] = email.utils.formatdate(localtime=True)
    mensaje['Message-ID'] = email.utils.make_msgid()
    mensaje.set_content("Esto es una prueba de email")
    
    with open("logoatc.gif", "rb") as f:
        gif = f.read()
    mensaje.add_attachment(gif, "image", "gif", filename="atc.gif")
    
    binario = mensaje.as_bytes()
    if not binario.endswith(b"\r\n"):
        binario += b"\r\n"
    datos_completos = binario + b".\r\n"
    
    print(datos_completos.decode("utf-8"))

    # enviar mensaje
    sc.sendall(datos_completos)
    RecvReply(sc, b"250")

    # QUIT
    time.sleep(0.1)
    sc.sendall(b"QUIT\r\n")
    RecvReply(sc, b"221")

    # Cerrar el socket TCP
    s.close()
    print("Correo enviado con éxito y conexión cerrada con exito!!")

if __name__ == "__main__":
    main()