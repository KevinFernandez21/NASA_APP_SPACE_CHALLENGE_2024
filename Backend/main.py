import numpy as np
import os
from obspy import read
from obspy.signal.invsim import cosine_taper
from obspy.signal.filter import highpass
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset
from scipy.signal import hilbert
from scipy.signal import medfilt, savgol_filter
import matplotlib.pyplot as plt
import noisereduce as nr

# Ruta al archivo .mseed
data_directory = input('Enter the path to mseed the file: ')
# data_directory = './data/lunar/training/data/S12_GradeA/xa.s12.00.mhz.1975-04-12HR00_evid00191.mseed'
mseed_file = f'{data_directory}'

# Leer el archivo mseed
st = read(mseed_file)
tr = st[0].copy()  # Obtener la primera traza

# Aplicar el filtro de banda
minfreq = 0.5
tr.filter('highpass', freq=minfreq)

# Obtener datos de la traza filtrada
tr_times = tr.times()
tr_data = tr.data

# Normalización Min-Max
min_val = np.min(tr_data)
max_val = np.max(tr_data)
tr_data_minmax = 2 * (tr_data - min_val) / (max_val - min_val) - 1  # Escalado entre -1 y 1

# 1. Aplicar un Filtro de Mediana
tr_data_median_filtered = medfilt(tr_data_minmax, kernel_size=5) 

# Visualizar las señales
plt.figure(figsize=(12, 8))

# Señal Filtrada con Mediana
plt.subplot(3, 1,1)
plt.plot(tr_times, tr_data_median_filtered, 'r-', label='Filtrada con Mediana')
plt.title('Señal Filtrada con Filtro de Mediana')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.savefig('mediana.png')
plt.legend()

plt.tight_layout()
# plt.show()

sample_rate = 1 / (tr_times[1] - tr_times[0])  # Calcular tasa de muestreo
signal_cleaned = nr.reduce_noise(y=tr_data_median_filtered, sr=sample_rate, time_mask_smooth_ms=40000)

plt.subplot(3, 1, 1)
plt.plot(tr_times, signal_cleaned , 'b-', label='Original')
plt.title('Señal Original')
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.legend()

plt.tight_layout()
# plt.show()


# Sampling frequency of our trace
df = tr.stats.sampling_rate

# How long should the short-term and long-term window be, in seconds?
sta_len = 400
lta_len = 4000

# Run Obspy's STA/LTA to obtain a characteristic function
cft = classic_sta_lta(signal_cleaned, int(sta_len * df), int(lta_len * df))

# Definir el tiempo mínimo de duración de los eventos (en segundos)
min_duration = 420 # Puedes ajustarlo según tus necesidades

# Convertir el tiempo mínimo de duración a muestras
min_duration_samples = int(min_duration * df)
# Plot characteristic function
fig,ax = plt.subplots(1,1,figsize=(12,3))
ax.plot(tr_times,cft)
ax.set_xlim([min(tr_times),max(tr_times)])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Characteristic function')
plt.savefig('caracteristica.png')
