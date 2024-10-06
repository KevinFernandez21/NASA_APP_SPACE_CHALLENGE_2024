import os
import tempfile
import numpy as np
from obspy import read
from obspy.signal.trigger import classic_sta_lta, trigger_onset
from scipy.signal import medfilt
import noisereduce as nr
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.post("/get-filtered-signals/")
async def get_filtered_signals(file: UploadFile = File(...)):
    # Crear un archivo temporal para almacenar el archivo subido
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        # Copiar el contenido del archivo subido al archivo temporal
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

        # Leer el archivo mseed
        st = read(temp_file_path)
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

        sample_rate = 1 / (tr_times[1] - tr_times[0])  # Calcular tasa de muestreo
        signal_cleaned = nr.reduce_noise(y=tr_data_median_filtered, sr=sample_rate, time_mask_smooth_ms=40000)

        # Sampling frequency of our trace
        df = tr.stats.sampling_rate

        # How long should the short-term and long-term window be, in seconds?
        sta_len = 60
        lta_len = 1200

        # Run Obspy's STA/LTA to obtain a characteristic function
        cft = classic_sta_lta(signal_cleaned, int(sta_len * df), int(lta_len * df))

        # Definir el tiempo mínimo de duración de los eventos (en segundos)
        min_duration = 420 # Puedes ajustarlo según tus necesidades

        # Convertir el tiempo mínimo de duración a muestras
        min_duration_samples = int(min_duration * df)
        
        l_threshold_on = [12,10,6,5,4,1.8,1.5,1.1]  # Lista de umbrales de activación
        l_threshold_off = [1,1,1,1,1,1,1,1]  # Lista de umbrales de desactivación

        filtered_on_off = []  # Inicializar la lista que almacenará los eventos filtrados
        idx = 0  # Inicializar el índice para las listas de umbrales

        # Bucle while que se ejecuta hasta que se encuentre una lista no vacía de eventos
        while len(filtered_on_off) == 0 and idx < len(l_threshold_on) :
            thr_on = l_threshold_on[idx]  # Obtener el umbral de activación actual
            thr_off = l_threshold_off[idx]  # Obtener el umbral de desactivación actual
            
            # Obtener los triggers usando los umbrales actuales
            on_off = np.array(trigger_onset(cft, thr_on, thr_off))
            
            # Filtrar los eventos que duran menos que el tiempo mínimo
            filtered_on_off = []
            for triggers in on_off:
                if (triggers[1] - triggers[0]) >= min_duration_samples:
                    filtered_on_off.append(triggers)
            
            # Convertir la lista filtrada de nuevo a un array de NumPy
            filtered_on_off = np.array(filtered_on_off)

            # Incrementar el índice para probar el siguiente conjunto de umbrales en caso de que no se haya encontrado ningún evento
            idx += 1

        filtered_on_off = np.array(filtered_on_off)
        filtered_on_off = filtered_on_off / df
        filtered_on_off_list = filtered_on_off.tolist()
        return JSONResponse(content={"filtered_signals": filtered_on_off_list})
    
    finally:
        file.file.close()  # Cerrar el archivo subido
        os.remove(temp_file_path)  # Eliminar el archivo temporal

