import socket

info = socket.getaddrinfo("en.wikipedia.org", "www")[0]

s = socket.socket(info[0], info[1], info[2])
s.connect(info[4])

s.sendall(b"GET / HTTP/1.1\r\nHost: en.wikipedia.org\r\n\r\n")
respuesta = s.recv(10000)
while (len(respuesta) > 0):
    print(str(respuesta, "utf-8"))
    respuesta = s.recv(10000)

