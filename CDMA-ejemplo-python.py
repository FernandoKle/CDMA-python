#!/usr/bin/python
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
#from scipy import io, integrate, linalg, signal
#from scipy.sparse.linalg import eigs

#Variables
n_datos = 3 # bits de datos
n_PN = 30 # bits de secuencia pseudo aletoria
n = 2 # cantidad de usuarios simultaneos

#Generacion de datos

#genera una matriz de enteros aletorios ente 0 y 1
datos = np.random.randint(2, size=(n_datos,n))
PN = np.random.randint(2, size=(n_PN,n))
#print(datos)
#print(PN)

#muestra los datos de cada usuario
for i in range(0,n):
    print("\ndatos del usuario",i)
    print(datos[:,i].transpose())
    print("Secuencia pseudo aleatoria del usuario",i)
    print(PN[:,i].transpose())

datos = 2 * datos - 1
signal = np.zeros((90,2))
# [:,i] -> vector columna i
for i in range(0,n): #de 0 hasta n - 1
    signal[:,i] = np.kron(datos[:,i],PN[:,i])

#print(signal)

PN_long = np.matlib.repmat( PN , n_datos , 1 )
#print(PN_long)

#repite los datos 100 veces
PN_plot = np.repeat(PN_long,100,1)
data_plot = np.repeat(datos,100,1) 
signal_plot = np.repeat(signal,100,1)

L = PN_plot.size
#print(L)

for i in range(0,n):
    plt.plot(data_plot[:,i])
    fig = plt.figure() #genera la figura
    ax = fig.add_subplot(3,1,1) #agrega el subplot
    #plt.show()
