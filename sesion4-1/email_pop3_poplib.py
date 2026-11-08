#!/usr/bin/env python3
import poplib
import getpass

def main():
    server = "pop.gmail.com" # no hace falta decir el puerto, es 995 por defecto

    # pedir usuario y contraseña por teclado
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")

    # instanciar el objeto POP3_SSL y activar la depuración del protocolo
    pop3_mail = poplib.POP3_SSL(server)
    pop3_mail.set_debuglevel(2)

    # enviar usuario y contraseña con user() y pass_()
    pop3_mail.user(username)
    pop3_mail.pass_(password)

    # recibir el contenido del primer mensaje con retr(1)
    # retr() retorna una tupla de 3 elementos: el número de mensaje, su contenido y el tamaño q ocupa
    resp, cont, tam = pop3_mail.retr(1)

    print(f"\nRespuesta del servidor: {resp}")
    print(f"Tamaño del mensaje: {tam} bytes\n")

    print("\nCONTENIDO DEL PRIMER MENSAJE:")
    for linea in cont: # contenido se almacena en una lista, siendo cada elemento una linea
        print(linea.decode('utf-8'))

    # Cerrar
    pop3_mail.quit()
    print("\nConexión POP3 cerrada con éxito.")

if __name__ == "__main__":
    main()