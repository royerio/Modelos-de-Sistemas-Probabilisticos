import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def energia_diaria(archivo_json):
    '''
    Importa la base de datos completa y devuelve un
    vector con la energía diaria, en MWh.
    '''
    
    # Cargar el "DataFrame"
    df = pd.read_json(archivo_json) 

    # Convertir en un array de NumPy
    datos = np.array(df)  

    # Crear vector con todos los valores horarios de demanda
    demanda = []

    # Extraer la magnitud de la demanda para todas las horas
    for hora in range(len(datos)):
        instante = datetime.fromisoformat(datos[hora][0]['fechaHora'])
        demanda.append(datos[hora][0]['MW'])

    # Separar las magnitudes en grupos de 24 (24 h)
    demanda = np.split(np.array(demanda), len(demanda) / 24)

    #Crear vector para almacenar la enegia a partir de la demanda
    energia = []

    #calcular la energia diaria por la Regla del Trapecio
    for dia in range(len(demanda)):

        E = round(np.trapz(demanda[dia]), 2)
        energia.append(E)

    return energia


##########################################################
def parametros_energia(vector_energia): # E
    '''
    Calcula los parámetros media y stDev
    en del vector de energía, y los retorna
    '''

    media = np.median(vector_energia)
    desviacion = np.std(vector_energia)

    return media, desviacion #mu, sigma
###########################################################

# Cargamos la energia
E = energia_diaria('demanda_2019.json')
E = np.array(E)
media, desviacion = parametros_energia(E)

print(media)
print(desviacion)
# Separamos la energia en grupos de 7
E = E[0:252]
E = np.split(E, 36) #energia, semanas


semanal = [] # (36, 1) vector de E semanal
for semana in range(36):
  Se = sum(E[semana])
  semanal.append(Se)

semanal = np.array(semanal)

Z = (semanal - (7 * media))/(np.sqrt(7)*desviacion)
print(Z)

plt.hist(Z)
plt.show()
