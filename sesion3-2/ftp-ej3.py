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

f_local = open("prueba-copia.txt", "wb") # Creamos el fichero local
                                         # importante abrirlo en modo binario "b"
result = f.retrbinary("RETR prueba.txt",    # Enviar petición de fichero
            f_local.write)      # Función a ejecutar por cada bloque recibido
f_local.close()
print(result)
