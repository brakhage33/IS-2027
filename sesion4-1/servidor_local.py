#!/usr/bin/env python3
import socket


# servidor local hecho con IA para probar el codigo con los portatiles

def iniciar_servidor():
    HOST = "127.0.0.1"
    PORT = 2525

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"[*] Servidor SMTP local robusto escuchando en {HOST}:{PORT}...")

    while True:
        conn, addr = server_socket.accept()
        print(f"\n[+] Conexión aceptada desde {addr}")
        
        try:
            conn.sendall(b"220 localhost ESMTP ready\r\n")

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                comando = data.decode('utf-8', errors='ignore').strip()
                print(f"  Recibido: {comando[:30]}...") # Imprime un resumen para no saturar

                if comando.startswith("HELO") or comando.startswith("EHLO"):
                    conn.sendall(b"250-localhost Hello\r\n250 OK\r\n")
                elif comando.startswith("MAIL FROM"):
                    conn.sendall(b"250 Sender ok\r\n")
                elif comando.startswith("RCPT TO"):
                    conn.sendall(b"250 Recipient ok\r\n")
                elif comando.startswith("DATA"):
                    conn.sendall(b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
                    
                    # Consumir todo el flujo del correo hasta encontrar el punto de fin (.)
                    datos_correo = b""
                    while b"\r\n.\r\n" not in datos_correo and b"\n.\n" not in datos_correo:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        datos_correo += chunk
                    
                    print(f"  [i] Mensaje con adjunto recibido correctamente ({len(datos_correo)} bytes).")
                    conn.sendall(b"250 Message accepted for delivery\r\n")
                    
                elif comando.upper() == "QUIT" or comando.startswith("QUIT"):
                    conn.sendall(b"221 Bye\r\n")
                    print("[-] Sesión cerrada ordenadamente.")
                    break
                else:
                    conn.sendall(b"250 OK\r\n")

        except Exception as e:
            print(f"[-] Error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    server_socket = None
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        print("\nServidor detenido.")