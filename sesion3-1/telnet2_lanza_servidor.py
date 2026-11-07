import getpass
import telnetlib
import time

HOST = "localhost"
PORT = 23
user = ""
password = ""

tn = telnetlib.Telnet(HOST, PORT)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.read_until(b"$")
tn.write(b"ps -ef\n")
procesos = tn.read_until(b"$")

if b"python3 udp_servidor3_con_ok" in procesos:
    print("El servidor ya está en ejecución")
    tn.write(b"exit\n")
else:
    tn.write(b"nohup python3 udp_servidor3_con_ok.py &\n")
    time.sleep(1)
    tn.write(b"exit\n")

print(tn.read_all().decode())
