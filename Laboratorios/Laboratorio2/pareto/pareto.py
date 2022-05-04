'''
Un ejemplo de como generar la CDF y la PDF para una
distribucion de datos aleatorios usando el modulo
scipy.stats
'''

#LIBRERIAS FUNDAMENTALES
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

'''
La distribucion de Pareto tiene un parametro b.
Vamos a elegir cualquier valor para b
'''
b = 2.62
#tamano del eje x:
x = np.linspace(stats.pareto.ppf(0.01, b), stats.pareto.ppf(0.99, b), 100)


pdf = stats.pareto.pdf(x, b)
cdf = stats.pareto.cdf(x, b)

#ploteando resultados
fig, ax = plt.subplots(1, 2, figsize = (12, 5), tight_layout = True)

#PDF
ax[0].set_title('Pareto PDF')
ax[0].plot(x, pdf, lw = 3, color = 'b')
ax[0].grid()

#CDF
ax[1].set_title('Pareto CDF')
ax[1].plot(x, cdf, lw = 3, color = 'r')
ax[1].grid()

#visualizando
plt.show()

