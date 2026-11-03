import dns.resolver

respuesta = dns.resolver.query('en.wikipedia.org')
print(respuesta[0].address)
print("Respuesta servidor:\n" + str(respuesta.response))
print("Respuesta servidor binaria:\n" + str(respuesta.response.to_wire()))
