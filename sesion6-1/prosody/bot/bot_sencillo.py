import asyncio
import slixmpp          # Biblioteca principal para XMPP
import logging          # Para el log de depuración
import getpass          # Para pedir la contraseña de forma segura
import os               # Para obtener variables de entorno (contraseña, para docker)
import ssl              # Para manejar certificados SSL

# Esta es la sintaxis de herencia en Python
class MyBot(slixmpp.ClientXMPP):
    # El constructor vuelve a su forma original.
    def __init__(self, jid, password):
        super().__init__(jid, password)

        # Registrar los eventos y sus manejadores
        self.add_event_handler("session_start", self.callback_para_session_start)
        self.add_event_handler("message", self.callback_para_message)
        self.add_event_handler("chatstate_active", self.callback_chatstate_active)
        self.add_event_handler("chatstate_composing", self.callback_chatstate_composing)
        self.add_event_handler("chatstate_paused", self.callback_chatstate_paused)
        self.add_event_handler("chatstate_inactive", self.callback_chatstate_inactive)

    # Implementación de los callbacks (todos son tipo async)
    async def callback_para_session_start(self, event):
        print("Sesión iniciada!")
        self.send_presence()
        
        # get_roster() es una corutina por lo que hay que usar 'await'
        await self.get_roster()
        print("Roster recibido.")

    async def callback_para_message(self, event):
        recibido = event['body']
        print(f"Recibido un mensaje de tipo {event['type']} de {event['from']}")
        print(f"Que dice: {recibido}")

        if event["type"] == "chat":
            msg = self.Message()
            msg["to"] = event["from"]
            msg["type"] = "chat"
            if recibido.startswith("="):
                try:
                    resultado = eval(recibido[1:])
                    msg["body"] = str(resultado)
                except Exception as e:
                    msg["body"] = f"Error: {e}"
            else:
                msg["body"] = f"¿{recibido}?"
            msg["chat_state"] = "active"
            msg.send()
    
    async def callback_chatstate_active(self, event):
        print(f"{event['from'].bare} está activo")

    async def callback_chatstate_composing(self, event):
        print(f"{event['from'].bare} está escribiendo...")

    async def callback_chatstate_paused(self, event):
        print(f"{event['from'].bare} ha parado de escribir")

    async def callback_chatstate_inactive(self, event):
        print(f"{event['from'].bare} está inactivo")

# Programa principal
if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    # Depuración
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')

    # Obtener credenciales
    jid = "bot@ingserv00"
    ip = "localhost"
    port = 5222
    clave = os.environ.get("CLAVEBOT")
    if clave is None:
        clave = getpass.getpass("Contraseña: ")

    # Manejo del certificado. Hay que extraer una copia de la que se generó
    # en el servidor
    cert_file = "localhost.crt"
    ssl_context = ssl._create_unverified_context()

    if os.path.exists(cert_file):
        print(f"Cargando certificado de confianza desde: {cert_file}")
        ssl_context.load_verify_locations(cert_file)
        
        # Desactivar la comprobación del nombre de host.
        # Esto es necesario porque el certificado es para 'ingservXX' pero conectamos a 'localhost'.
        print("Desactivando la comprobación de hostname.")
        ssl_context.check_hostname = False
    else:
        # Incluso podemos confiar ciegamente en el certificado, sin tener uno instalado en el cliente
        print(f"ADVERTENCIA: No se encontró '{cert_file}'. Desactivando TODA la validación de certificado.")
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

    # Instanciar el bot
    client = MyBot(jid, clave)

    # Asignar el contexto SSL a la instancia del cliente
    client.ssl_context = ssl_context
    client.register_plugin("xep_0085")
    
    # Conectar el bot al servidor
    client.connect((ip, port))
    
    # Iniciar el bucle de eventos.
    client.process(forever=True)
