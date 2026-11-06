# Comenzamos por definir el callback, que es una función
# que sera llamada por cada linea recibida del servidor
# Este callback se limita a acumular las lineas en una
# variable global llamada lista

lista = []

def acumular(linea):
    lista.append(linea)

import ftplib, getpass

clave = getpass.getpass("Clave? ")

f = ftplib.FTP("localhost")  # Conecta al servidor
f.login("uo297118", clave)   # Enviá comandos USER y PASS
f.cwd("prueba")             # Enviá comando CWD

# Borramos la lista donde recibiremos la respuesta
lista = []
# Enviamos comando LIST e indicamos el callback para tratar la respuesta
resp = f.retrlines("MLSD", acumular)

# Mostramos los resultados
print("Respuesta del protocolo: ", resp)
print("Contenidos de la carpeta remota:")
for l in lista:
    v = l.split(";")
    if (not (v[0] in ["type=dir", "type=pdir", "type=cdir"])):
        print(v[7])
        
