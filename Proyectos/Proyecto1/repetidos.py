from contextlib import ContextDecorator
import numpy as np
from numpy.lib.function_base import append

datos = ['145', '2784', '946', '256', '1784', '23', '2545', '25', '18', '36', '32', '42', '33', '38']

primerdigitoflotante = np.empty(np.shape(datos))
for i, d in enumerate(datos):
    primerdigitoflotante[i] = d[0]
#print(primerdigitoflotante)

primerdigito = primerdigitoflotante.astype(int)
print(primerdigito)

def cantidad(int):
    rep = {}
    for c in primerdigito:
        rep[c] = rep.get(c) + 1
    contador = 0
    for k in rep:
        if(rep[k]>1):
            contador += 1
    return(cantidad)
print(cantidad)