#!/usr/bin/env python3
import poplib
import getpass
import email.message
import email.header

def imprime_resumen_mensaje(msg_bytes):
    # Parsear los bytes recibidos y construir un objeto EmailMessage
    msg = email.message_from_bytes(msg_bytes)
    
    # Extraemos las cabeceras "From" y "Subject"
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")
    
    # Decodificar cabeceras con caracteres no-ascii / unicode
    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))
    
    # Extraemos el cuerpo del mensaje
    cuerpo = msg.get_payload()
    
    # Si es multi-part, nos quedamos con el primer elemento
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        cuerpo = "---Multipart. Parte 1\n" + parte_1
        
    # Imprimimos el resumen (cabeceras y primeros caracteres)
    print("From:", remite)
    print("Subject:", asunto)
    if isinstance(cuerpo, str):
        print(cuerpo[:500])
        if len(cuerpo) > 500:
            print("...[omitido]")
    else:
        print("[Contenido no textual]")
    print("-" * 80)

def main():
    server = "pop.gmail.com"

    # Pedir usuario y contraseña por teclado
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")

    # Instanciar el objeto POP3_SSL
    pop3_mail = poplib.POP3_SSL(server)
    pop3_mail.set_debuglevel(0) # Desactivamos depuración verbose para ver limpio el resumen

    # Enviar usuario y contraseña
    pop3_mail.user(username)
    pop3_mail.pass_(password)

    # Obtener el número total de mensajes disponibles con stat()
    num_mensajes, _ = pop3_mail.stat()
    print(f"\nTotal de mensajes en la bandeja: {num_mensajes}\n")

    # Recorrer todos los mensajes disponibles
    for i in range(1, num_mensajes + 1):
        print(f"--- MENSAJE {i} de {num_mensajes} ---")
        # retr(i) devuelve tupla: (respuesta, lista_de_lineas, tamaño)
        resp, cont, tam = pop3_mail.retr(i)
        
        # Convertir la lista de líneas de poplib a un array de bytes usando b"\r\n".join()
        msg_bytes = b"\r\n".join(cont)
        
        # Llamar a la función para imprimir el resumen correctamente formateado
        imprime_resumen_mensaje(msg_bytes)

    # Cerrar sesión
    pop3_mail.quit()
    print("\nConexión POP3 cerrada con éxito.")

if __name__ == "__main__":
    main()