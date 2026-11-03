import dns.resolver

respuesta = dns.resolver.query('www.google.com')


for ip in respuesta:
    print(ip) 

#print(respuesta.rrset)
