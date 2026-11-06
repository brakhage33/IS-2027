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

lista = []
resp = f.retrlines("MLSD", acumular)

for l in lista:
    v = l.split(";")
    if (not (v[0] in ["type=dir", "type=pdir", "type=cdir"])):
        nombre = v[7].strip(" ")
        f_local = open(nombre, "wb")
        result = f.retrbinary("RETR " + nombre, f_local.write)
        f_local.close()
        print(result)


