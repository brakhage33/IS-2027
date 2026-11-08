import dns.resolver

#respuesta = dns.resolver.query('www.google.com')
#respuesta = dns.resolver.query("gmail.com", "MX") -> DeprecationWarning: please use dns.resolver.resolve() instead
respuesta = dns.resolver.resolve('gmail.com', 'MX')

for rdata in sorted(respuesta, key=lambda x: x.preference): # ordenar por prioridad (preference)
    servidor = str(rdata.exchange).rstrip('.')
    ip = dns.resolver.resolve(servidor, 'A')[0].address
    print(f"{rdata.preference} {servidor}. {ip}")

#print(respuesta.rrset)
