import email.message, email.policy, email.utils
import smtplib
import getpass

# variables: servidor, puerto, direccion to y from
server = "smtp.gmail.com"
port = 587
correo = "emma.sanchez.couso@gmail.com"
fromaddr = correo
toaddr = correo

# instanciar un objeto de la clase SMTP
s = smtplib.SMTP(server, port)

# activar depuracion
s.set_debuglevel(1)

# usar la función starttls()
s.starttls() # (smtplib gestiona el wrap_socket internamente con s.starttls(), por lo que podemos usar s directamente

# pedir autentificacion por teclado
username = input("Usuario: ")
password = getpass.getpass("Contraseña: ")

# usar la función login()
s.login(username, password)

# construir mensaje
mensaje = email.message.EmailMessage()
mensaje['To'] = 'Desti Natario <destinatario@example.com>'
mensaje['From'] = 'Remi Tente <remitente@example.com>'
mensaje['Subject'] = 'Mensaje de prueba'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Esto es una prueba")
with open("logoatc.gif", "rb") as f:
    gif = f.read()
mensaje.add_attachment(gif, "image", "gif", filename="atc.gif")

# pasar mensaje a binario
binario = mensaje.as_bytes()

# imprimir mensaje pasando el binario a utf8 para que sea legible
#print(binario.decode("utf-8"))

# enviar mensaje binario a traves del socket
s.sendmail(fromaddr, toaddr, binario)

# cerrar conexion
s.close()