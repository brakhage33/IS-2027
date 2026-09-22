import socket


"""
El socket devuelto por esta función es un objeto en python (a diferencia
del C donde era un entero).

La mayoría de las funciones que operan sobre este socket serán métodos
de este objeto.
"""

# UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

"""
AF_INET -> IPv4
SOCK_DGRAM -> UDP

Para TCP sería:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""


"""
bind() asocia el socket a una dirección y puerto local.

El socket no se pasa como parámetro, sino que bind() es un método
del objeto socket.

La dirección y puerto es una tupla de dos elementos:
(1) dirección
(2) puerto
"""

s.bind(("", 8080))


"""
listen() convierte el socket en pasivo TCP.

Recibe como parámetro el número máximo de conexiones que pueden
quedar pendientes de ser aceptadas.

Solo se utiliza con TCP.
"""

s.listen(5)


"""
accept() espera clientes de un socket TCP.

Retorna dos resultados:
(1) el nuevo socket para comunicarnos con el cliente
(2) una tupla (dirección, puerto) del cliente
"""

cliente, origen = s.accept()


"""
connect() establece una conexión con otro socket TCP.

Recibe como parámetro una tupla:
(dirección, puerto)
"""

s.connect(("127.0.0.1", 8080))


"""
send() se utiliza para sockets TCP.

Recibe un único parámetro: una cadena de bytes de Python.

Devuelve el número de bytes que realmente se han enviado.

IMPORTANTE:
send() puede enviar menos bytes de los que contiene el mensaje.
"""

s.send(b"Este mensaje se envia por el socket")


"""
sendall() se utiliza para sockets TCP.

Se encarga de enviar todos los bytes.
Internamente realiza las llamadas necesarias a send().
"""

s.sendall(b"Este mensaje se envia completo")


"""
recv() se utiliza para sockets TCP.

Recibe como parámetro el número MÁXIMO de bytes que queremos recibir.

Devuelve una cadena de bytes con los bytes recibidos.

Si no hay bytes disponibles, se bloquea hasta que lleguen.

Si devuelve b"" significa que el otro extremo ha cerrado
el socket (fin de transmisión).
"""

datos = s.recv(1024)

print("Bytes recibidos:", len(datos))

if len(datos) == 0:
    print("El otro extremo ha cerrado el socket")


"""
TCP es un flujo de bytes.

recv(1024) NO significa que vaya a recibir exactamente 1024 bytes,
sino que recibirá como máximo 1024 bytes.

Un mensaje enviado mediante send() o sendall() puede recibirse
dividido entre varias llamadas a recv().
"""


"""
sendto() se utiliza para sockets UDP.

Recibe dos parámetros:

1. Una cadena de bytes con los datos que queremos enviar.
2. Una tupla (dirección, puerto) con el destino.

Ejemplo:
"""

s.sendto(b"Hola", ("127.0.0.1", 8080))


"""
recvfrom() se utiliza para sockets UDP.

Recibe como parámetro un entero indicando el número MÁXIMO de bytes
esperados en el datagrama.

Retorna una tupla con dos elementos:

1. Los bytes recibidos.
2. Una tupla (dirección, puerto) con el origen del datagrama.
"""

datagrama, origen = s.recvfrom(1024)

print("Se ha recibido un datagrama desde", origen)
print("Contiene lo siguiente:")
print(datagrama.decode("utf-8"))

# Ahora lo devolvemos a modo de eco
s.sendto(datagrama, origen)


"""
2.3 ¿Cadenas o bytes?

En Python3 tenemos dos tipos de cadenas importantes:

str   -> cadenas de caracteres
bytes -> cadenas de bytes

Una cadena str se escribe, por ejemplo:
"""

texto = "Hola ñ"


"""
Una cadena bytes se escribe poniendo una b delante:
"""

datos = b"Hola"


"""
Las cadenas str son texto Unicode.

Las cadenas bytes son secuencias de bytes.
Python no interpreta qué significan esos bytes.

Los bytes podrían representar:
- texto
- una imagen
- un sonido
- cualquier otro tipo de información binaria
"""


"""
De str a bytes:

Para convertir un str a bytes necesitamos indicar el encoding.

Por ejemplo:
"""

a = "ñ"

print(bytes(a, "utf8"))
# b'\xc3\xb1'

print(bytes(a, "latin1"))
# b'\xf1'


"""
También podemos utilizar el método encode().
"""

a = "ñ"

print(a.encode("utf8"))
# b'\xc3\xb1'


"""
De bytes a str:

Para convertir bytes a str necesitamos conocer el encoding
que se utilizó para crear esos bytes.

Podemos utilizar str():
"""

a = b"\xc3\xb1"

print(str(a, "utf8"))
# 'ñ'

print(str(a, "latin1"))
# 'Ã±'


"""
También podemos utilizar el método decode().
"""

a = b"\xc3\xb1"

print(a.decode("utf8"))
# 'ñ'


"""
Regla general:

Cuando trabajamos con texto, lo recomendable es convertir los bytes
a str lo antes posible después de recibirlos.

Y convertir el str a bytes justo antes de enviarlo.

Es decir:

bytes -> decode() -> str

str -> encode() -> bytes
"""


"""
Ejemplo de recepción de texto mediante un socket TCP:

Recibimos bytes
"""

texto = s.recv(50)

# Los convertimos inmediatamente a str
texto = texto.decode("utf8")

# A partir de aquí trabajamos con str
print("Texto recibido:", texto)


"""
Ejemplo de envío de texto mediante un socket TCP:

La variable texto contiene un str.
Por ejemplo, podría haberse obtenido mediante input().
"""

texto = "Hola mundo"

# Convertimos a bytes justo antes de enviarlo
enviados = s.send(texto.encode("utf8"))

"""
CUIDADO:

La variable enviados contiene el número de BYTES enviados,
no el número de caracteres.
"""


"""
Por ejemplo, con el carácter ñ:

"""

texto = "ñ"

print(len(texto))
# 1 carácter

print(len(texto.encode("utf8")))
# 2 bytes


"""
Esto ocurre porque UTF-8 utiliza un número variable de bytes
para representar los caracteres Unicode.

Por ejemplo:

ASCII:
a -> 1 byte

UTF-8:
ñ -> 2 bytes
€ -> 3 bytes
"""


"""
PROBLEMA DE TCP Y UTF-8

Si hacemos:

texto = s.recv(50)
texto = texto.decode("utf8")

podría ocurrir que nos hayan enviado más de 50 bytes.

TCP es un flujo de bytes, por lo que los datos pueden dividirse
de cualquier manera entre diferentes llamadas a recv().

Además, puede ocurrir que el byte número 50 sea parte de un
carácter UTF-8 de varios bytes.

En ese caso, al hacer decode() podríamos tener una secuencia
UTF-8 incompleta y producirse un error.

Este problema aparece en TCP porque TCP trabaja como un flujo.

En UDP no ocurre de la misma manera porque los datos se organizan
en datagramas.

Un datagrama se recibe como una unidad mediante recvfrom().
"""


"""
RESUMEN:

TCP:
    socket(AF_INET, SOCK_STREAM)
    bind()
    listen()
    accept()
    connect()
    send()
    sendall()
    recv()

UDP:
    socket(AF_INET, SOCK_DGRAM)
    bind()
    sendto()
    recvfrom()

Conversión de texto:

    str -> encode() -> bytes

    bytes -> decode() -> str
"""


"""
Ejemplo mínimo de servidor UDP:

"""

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(("", 8080))

datagrama, origen = s.recvfrom(1024)

print("Se ha recibido un datagrama desde", origen)
print("Contiene:", datagrama.decode("utf8"))

s.sendto(datagrama, origen)
