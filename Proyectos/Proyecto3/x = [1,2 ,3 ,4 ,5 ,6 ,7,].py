import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from fitter import Fitter
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

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

#Seguido, averiguo las horas a las que debo trabajar
#Mi numero de carné es A43333.

import random
digitos = 43333
def horas_asignadas(digitos):
    '''Elige una hora A en periodo punta
    y una hora B de los otros periodos,
    con los dígitos del carné como "seed"
    '''
    
    random.seed(digitos)
    punta = [11, 12, 18, 19, 20]
    valle = [7, 8, 9, 10, 13, 14, 15, 16, 17]
    nocturno = [21, 22, 23, 0, 1, 2, 3, 4, 5, 6]
    otro = valle + nocturno
    HX = punta[random.randrange(0, len(punta))]
    HY = otro[random.randrange(0, len(otro))]
    horas = 'Mi hora X: {}, Mi hora Y: {}'.format(HX, HY)
    return horas

mis_horas = horas_asignadas(digitos)
print(mis_horas)


hora1 = 18
hora2 = 8

# Se eligen las dos horas que desean estudiarse
hora_1 = extraer_datos('demanda_2019.json', hora1) 
hora_2 = extraer_datos('demanda_2019.json', hora2) 



def distribucion_conjunta(X, Y, bins):
    '''Pide por parámetros dos variables aleatorias
    X y Y, así como el número de 'bins' o divisiones
    a emplear para construir el histograma bivariado.
    Crea una gráfica y retorna dos tablas de datos de
    pares ordenados x, y y su probabilidad p asociada.
    '''
    np.seterr(all='ignore') # ignorar advertencias
    
    # Se inicializa la figura interactiva 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Se obtiene el plano de probabilidades para graficar el hist3D
    hist, xbins, ybins = np.histogram2d(X, Y, bins=bins, normed=False)
    hist = hist / sum(sum(hist))
    xbins = (xbins + np.roll(xbins, -1))[:-1] / 2.0 
    ybins = (ybins + np.roll(ybins, -1))[:-1] / 2.0 
    
    #Formatos de retorno para la funcion de densidad bivariada discreta
    xyp = [[xbins[i], ybins[j], hist[i][j]] for i in range(bins) for j in range(bins)]
    xy = hist 

    # Se construyen los arreglos para el ancho de Bins * Bins barras
    xpos, ypos = np.meshgrid(xbins, ybins, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    # Se dimensiona el ancho visual de las barras (como un sólido).
    dx = dy = 30 * np.ones_like(zpos)
    dz = hist.ravel() 

    # Se visualiza el histograma 3D
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
    ax.set_xlabel('La hora 1, $X$')
    ax.set_ylabel('La hora 2, $Y$')
    ax.set_zlabel('Probabilidad')
    plt.show()

    return xyp, xy, xbins, ybins



# Se ejecuta el análisis bivariado
xyp, xy, xbins, ybins = distribucion_conjunta(hora_1, hora_2, bins = 10)









#Sección 4.1.2. Determine las funciones de densidad marginales 𝑓𝑋(𝑥)  y  𝑓𝑌(𝑦)  
#a partir de los datos y utilizando un modelo de mejor ajuste.


def evaluar_modelos(datos):
    '''Evalúa las 80 distribuciones del módulo stats
    y obtiene el el modelo de mejor ajuste para
    la demanda anual de una hora específica. Retorna
    el nombre de la mejor distribución y una tupla con
    los parámetros del modelo.
    '''
    
    np.seterr(all='ignore') # ignorar advertencias
    
    # Hallar el mejor ajuste con Fitter
    f = Fitter(datos, timeout=120)
    f.fit()
    ajuste = f.get_best()
    
    for i in ajuste.keys():
        dist, params = i, ajuste[i]

    print('------------\nDistribución\n------------')
    print(dist, '\n')
    print('----------\nParámetros\n----------')
    print(params)

    return dist, params

#Se realiza el llamada para obtener los parametros del mejor ajuste para las horas implementadas
distx, paramsx = evaluar_modelos(hora_1)
disty, paramsy = evaluar_modelos(hora_2)

def densidad_marginal(xy, bins, dist, params, eje):
    '''Se elige eje='x' o eje='y' según sea el caso para la 
    densidad marginal en Y o en X. El parámetro 'xy' es la
    tabla de datos, 'bins' es el vector de valores de potencia 
    xbins o ybins. Los parámetros 'dist' y 'params' corresponden
    al modelo de mejor ajuste retornado por el fitter.
    '''
    
    np.seterr(all='ignore') # ignorar advertencias
    
    # Hallar la densidad marginal de X o Y, según se indique en 'eje'
    if eje == 'x':
        filas = len(xy)
        marginal = [sum(xy[i]) for i in range(filas)]
    elif eje == 'y':
        xy = xy.transpose()
        filas = len(xy)
        marginal = [sum(xy[i]) for i in range(filas)]

    # Visualizar modelo de mejor ajuste
    distro = getattr(stats, dist) 
    d = np.arange(min(bins)*0.96, max(bins)*1.04, 1)
    pdf_plot = distro.pdf(d, *params)
    plt.plot(d, pdf_plot*22, lw=3.5, color='r')
    
    # Visualizar función de densidad marginal
    plt.bar(bins, marginal, width=12)
    plt.title('Contraste: densidad marginal vs. modelo de mejor ajuste')
    plt.xlabel('Potencia [MW]')
    plt.ylabel('Densidad Probabilística')
    plt.show()
    
    return marginal


# Se contrasta la densidad marginal para cada hora, según su eje
dmx = densidad_marginal(xy, xbins, distx, paramsx, eje='x')
dmy = densidad_marginal(xy, ybins, disty, paramsy, eje='y')





#4.1.3 Determine los valores esperados  𝐸[𝑋]  y  𝐸[𝑌]  de los datos

#Determinar el consumo energético promedio para las horas
EX1 = np.mean(hora_1)
print("El consumo energético promedio para la hora", hora1, ":")
print(EX1, "MWh")

#Determinar el consumo energético promedio para las horas
EX2 = np.mean(hora_2)
print("El consumo energético promedio para la hora", hora2, ":")
print(EX2, "MWh")