import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from fitter import Fitter
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

hora_1 = 11
hora_2 = 13

def extraer_datos(archivo_json, hora):
    '''Importa la base de datos completa y devuelve los
    datos de potencia a la hora indicada en un
    array de valores.
    '''
    
    # Cargar el "DataFrame"
    df = pd.read_json(archivo_json) 
    
    # Convertir en un array de NumPy
    datos = np.array(df)     
    

    # Crear vector con los valores demanda en una hora
    demanda = []

    # Extraer la demanda en la hora seleccionada
    for i in range(len(datos)):
        instante = datetime.fromisoformat(datos[i][0]['fechaHora'])
        if instante.hour == hora:
            demanda.append(datos[i][0]['MW'])

    return demanda


    #Se realiza la extracción de los datos del archivo.json para las horas 11 y 13
    datoshx = extraer_datos('demanda_2019.json', hora_1)
    datoshy = extraer_datos('demanda_2019.json', hora_2)

        

    # Separar las magnitudes en grupos de 24 (24 h)
    demanda = np.split(np.array(demanda), len(demanda) / 24)
    


    
    # Crear vector para almacenar la enegia a partir de la demanda
    energia = []

    # Calcular la energia diaria por la regla del trapecio
    for dia in range(len(demanda_2019.json)):
        E = round(np.trapz(demanda[dia]), 2)
        energia.append(E)
    
    return(energia)
    print("La energia diaria es de:", energia)
    
    energia_semana = energia*7

    vector = len(energia)

    print(vector)