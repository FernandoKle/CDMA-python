#!/usr/bin/python

# Librerias
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
#from scipy import io, integrate, linalg, signal
#from scipy.sparse.linalg import eigs

# Parametros 
n_datos = 3 # bits de datos
n_PN = 30 # bits de secuencia pseudo aletoria
n = 2 # cantidad de usuarios simultaneos
pi = np.pi # pi = 3.141592653589793

# Variables 
#Generacion de datos
#genera una matriz de enteros aletorios ente 0 y 1
datos = np.random.randint(2, size=(n ,n_datos))#datos de cada usuario 
PN = np.random.randint(2, size=(n, n_PN))#secuencia pseudo aleatoria de cada usuario
#print(datos)
#print(PN)

#muestra los datos y la secuencia pseudo aleatoria de cada usuario
for i in range(n):
    print("\ndatos del usuario",i)
    print(datos[:].transpose())
    #Toma la columna i de la matriz datos y con transpose() la escribe en forma de vector (horizontal)
    print("Secuencia pseudo aleatoria del usuario",i)
    print(PN[:,i].transpose())
   
# Cambia los 0 (ceros) por -1 (menos uno)
bindata = 2 * datos - 1

# declara la variable signal y la rellena con zeros.
signal = np.zeros((n,90))


for i in range(n): #de 0 hasta n - 1
  	# [:,i] -> vector columna i
    signal[i,:] = np.kron(bindata[i,:],PN[i,:])

# copia la mariz PN n_datos veces
PN_long = np.matlib.repmat( PN , 1 , n_datos )
#print(PN_long)

# repite los datos 100 veces
PN_plot = np.repeat(PN_long,100,1)
data_plot = np.repeat(bindata,100,1) 
signal_plot = np.repeat(signal,100,1)

L = data_plot.size # no se usa ?


# Grafica los datos de cada usuario, la secuencia pseudo aleatoria que les corresponde y la senial codificada que le corresponde.
for i in range(n):
    fig = plt.figure() # genera la figura

    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.set_size_inches(18.5, 10.5, forward=True)
    fig.tight_layout(pad=2.0)
    x = np.arange(0, 3, 0.01)   # rango de x
    # ax1 = fig.add_subplot(5,1,1) # agrega el subplot, ax por axys (eje)
    ax1.set_title("Datos, usuario: " + str(i) )
    plt.xticks(np.arange(0, 4, step=1))  # definicion de x en el grafico
    ax1.plot(x, data_plot[i, :], linewidth=2)
    
    x = np.arange(0, 3, 0.001/3)  


    # ax2 = fig.add_subplot(3,1,2) # agrega otro subplot
    plt.xticks(np.arange(0, 4, step=1)) 
    ax2.set_title("Secuencia pseudo aleatoria")
    ax2.plot(x, PN_plot[i ,:])
    
    x = np.arange(0, 3, 0.001/3)
    # ax3 = fig.add_subplot(3,1,3) # agrega otro subplot
    plt.xticks(np.arange(0, 4, step=1)) 
    ax3.set_title("Señal codificada")
    ax3.plot(x, signal_plot[i,:])

    fig.show()
    
# Combinacion de señales

senial_transmisora = signal.sum(axis=0) #sum(signal, 2)
senial_transmisora_plot = signal_plot.sum(axis=0) #sum(signal, 2)
#print(signal)
#print(type(signal))
#print(senial_transmisora)

fig = plt.figure()
fig.set_size_inches(18.5, 10.5, forward=True)
ax1 = fig.add_subplot(3,1,1)
x = np.arange(0, 3, 0.001/3)
plt.xticks(np.arange(0, 4, step=1))
ax1.plot(x, senial_transmisora_plot ,linewidth=3)
ax1.set_title("Señal a transmitir" )
fig.show()

# Espectros

# numpy -> Start , Stop , Step	; matlab -> start : step : stop
f_data = np.arange( - pi , pi - ( 2 * pi / datos.size ) , 2 * pi / datos.size ) #f_data = -pi:2*pi/length(data):pi-2*pi/length(data);
f_signal = np.arange( - pi , pi - ( 2 * pi / signal.size ) , 2 * pi / signal.size )	# f_signal = -pi:2*pi/length(signal):pi-2*pi/length(signal);

freqs = np.fft.fftfreq(64, 0.1)
# Grafica del espectro

fig = plt.figure()

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
fig.tight_layout(pad=1.0)
fig.set_size_inches(18.5, 10.5, forward=True)

ax1.set_title("FFT de los datos del usuario 1")
ax1.stem(freqs, np.abs( np.fft.fft( bindata[0, :], 64) ) / datos.size )


#plt.xlim( 0 , 2 * pi )
ax2.set_title("FFT de la senial transmitida del usuario 1")
ax2.stem( freqs, np.abs( np.fft.fft( signal[0, :], 64 ) ) / signal.size )

ax3.set_title("FFT de los datos del usuario 2")
ax3.stem(freqs, np.abs( np.fft.fft( bindata[1, :], 64) ) / datos.size )



#plt.xlim( 0 , 2 * pi )
ax4.set_title("FFT de la senial transmitida del usuario 2")
ax4.stem( freqs, np.abs( np.fft.fft( signal[1, :], 64 ) ) / signal.size )

# Decodificacion

decoded_signal = np.zeros(( n_PN , n_datos , n_PN )) # Que esta pasando aca, en que parte de la teoria hay matrices 3D !?
recovered_signal = np.zeros(( n , n_PN ))

for user in range(n):

  decoded_signal[user,:] = np.reshape( senial_transmisora , [ n_datos , n_PN ] ) * PN[user,:] 
  print("\n",decoded_signal[user,:])

  #for i in range(n_datos):
    #print("\n",decoded_signal[user,i]) # decoded_signal[user,i] es un vector, por cada usuario hay n_datos vectores en decoded_signal
    #for val in decoded_signal[user,i]:
      #if val > 0:
        #recovered_signal[user,i] = 1
      #elif val <= 0:
       # recovered_signal[user,i] = 0

  print(decoded_signal[user,:] > 0)
  #recovered_signal[user,:] = decoded_signal[user,:] > 0
  print("\n",recovered_signal[user,:])

    #decoded_signal(:,user) = (reshape(transmittesr_signal,[n_PN n_data])'*PN(:,user));
    #recovered_signal(decoded_signal(:,user) > 0) = 1;
    #recovered_signal(decoded_signal(:,user) <= 0) = 0;
    
# Graficas de la senial decodificada
  
decoded_signal_plot = np.repeat( decoded_signal[user,:] , 500, 1)
recovered_signal_plot = np.repeat( recovered_signal, 500, 1 )

fig = plt.figure()
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)

fig.tight_layout(pad=1.0)
fig.set_size_inches(18.5, 10.5, forward=True)


plt.xticks(np.arange(0, 4, step=1))
x = np.arange(0, 3, 0.001/3)
ax1.plot(x, senial_transmisora_plot, linewidth = 3)
ax1.set_title("senial recibida")

plt.xticks(np.arange(0, 4, step=1))
x = np.arange(0, 3, 0.001/3)  
ax2.plot(x, PN_plot[user,:] , linewidth = 3)
ax2.set_title("Secuencia pseudo aleatoria")


ax3.plot(recovered_signal_plot , linewidth = 3)
ax3.set_title("Senial decodificada")


ax4.plot(data_plot[user,:] , linewidth = 3)
ax4.set_title("Datos originales")

fig.show()

# Fin
