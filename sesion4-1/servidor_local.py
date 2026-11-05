#!/usr/bin/env python3
import socket

# servidor local hecho con IA para probar el codigo con los portatiles

def iniciar_servidor():
    HOST = "127.0.0.1"
    PORT = 2525

    # Crear el socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"[*] Servidor SMTP local escuchando en {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"[+] Conexión aceptada desde {addr}")
        
        try:
            # 1. Enviar saludo inicial SMTP (Código 220 esperado por tu cliente)
            conn.sendall(b"220 localhost ESMTP ready\r\n")

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                comando = data.decode('utf-8', errors='ignore').strip()
                print(f"  Recibido del cliente: {comando}")

                # 2. Responder según el comando SMTP recibido
                if comando.startswith("HELO") or comando.startswith("EHLO"):
                    conn.sendall(b"250 OK\r\n")
                elif comando.startswith("MAIL FROM"):
                    conn.sendall(b"250 Sender ok\r\n")
                elif comando.startswith("RCPT TO"):
                    conn.sendall(b"250 Recipient ok\r\n")
                elif comando.startswith("DATA"):
                    # El servidor indica que está listo para recibir el contenido (Código 354)
                    conn.sendall(b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
                elif "." in comando: 
                    # Fin del bloque DATA (marcado con un punto solo)
                    conn.sendall(b"250 Message accepted for delivery\r\n")
                elif comando.startswith("QUIT"):
                    conn.sendall(b"221 Bye\r\n")
                    print("[-] Sesión cerrada ordenadamente por el cliente.")
                    break
                else:
                    conn.sendall(b"500 Command unrecognized\r\n")

        except Exception as e:
            print(f"[-] Error en la conexión: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    iniciar_servidor()