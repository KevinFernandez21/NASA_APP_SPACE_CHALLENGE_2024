import json
import os
import tempfile
import numpy as np
from obspy import read, Trace, UTCDateTime, Stream
from obspy.signal.trigger import classic_sta_lta, trigger_onset
from scipy.signal import medfilt
import noisereduce as nr
from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
from obspy import read
import io
import matplotlib.pyplot as plt

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
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

        st = read(temp_file_path)
        tr = st[0].copy()

        minfreq = 0.5
        tr.filter("highpass", freq=minfreq)
        tr_times = tr.times()
        tr_data = tr.data

        min_val = np.min(tr_data)
        max_val = np.max(tr_data)
        tr_data_minmax = (
            2 * (tr_data - min_val) / (max_val - min_val) - 1
        )  # Escalado entre -1 y 1

        # 1. Aplicar un Filtro de Mediana
        tr_data_median_filtered = medfilt(tr_data_minmax, kernel_size=5)

        sample_rate = 1 / (tr_times[1] - tr_times[0])  # Calcular tasa de muestreo
        signal_cleaned = nr.reduce_noise(
            y=tr_data_median_filtered, sr=sample_rate, time_mask_smooth_ms=40000
        )

        # Sampling frequency of our trace
        df = tr.stats.sampling_rate

        # How long should the short-term and long-term window be, in seconds?
        sta_len = 60
        lta_len = 1200

        # Run Obspy's STA/LTA to obtain a characteristic function
        cft = classic_sta_lta(signal_cleaned, int(sta_len * df), int(lta_len * df))

        # Definir el tiempo mínimo de duración de los eventos (en segundos)
        min_duration = 420  # Puedes ajustarlo según tus necesidades

        # Convertir el tiempo mínimo de duración a muestras
        min_duration_samples = int(min_duration * df)

        l_threshold_on = [
            12,
            10,
            6,
            5,
            4,
            1.8,
            1.5,
            1.1,
        ]  # Lista de umbrales de activación
        l_threshold_off = [1, 1, 1, 1, 1, 1, 1, 1]  # Lista de umbrales de desactivación

        filtered_on_off = (
            []
        )  # Inicializar la lista que almacenará los eventos filtrados
        idx = 0  # Inicializar el índice para las listas de umbrales

        # Bucle while que se ejecuta hasta que se encuentre una lista no vacía de eventos
        while len(filtered_on_off) == 0 and idx < len(l_threshold_on):
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
        file.file.close()
        os.remove(temp_file_path)


@app.post("/upload-mseed-to-csv/")
async def upload_and_square(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

        st = read(temp_file_path)
        tr = st[0].copy()

        tr_times = tr.times()
        tr_data = tr.data

        min_val = np.min(tr_data)
        max_val = np.max(tr_data)
        tr_data_minmax = 2 * (tr_data - min_val) / (max_val - min_val) - 1

        output = io.StringIO()

        output.write("time,normalized_data\n")

        for i in range(len(tr_times)):
            output.write(f"{tr_times[i]},{tr_data_minmax[i]}\n")
        output.seek(0)

        response = StreamingResponse(output, media_type="text/csv")
        response.headers["Content-Disposition"] = (
            f"attachment; filename={file.filename.split('.')[0]}_normalized.csv"
        )
        return response

    except Exception as e:
        return {"error": str(e)}
    finally:
        temp_file.close()


@app.post("/upload-csv-to-mseed/")
async def upload_and_square(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

        data = np.genfromtxt(temp_file_path, delimiter=",", skip_header=1)
        times = data[:, 0]
        normalized_data = data[:, 1]

        min_val = np.min(normalized_data)
        max_val = np.max(normalized_data)
        tr_data = (normalized_data + 1) * (max_val - min_val) / 2 + min_val

        tr = Trace(data=tr_data)
        tr.stats.starttime = UTCDateTime(times[0])
        tr.stats.sampling_rate = 1 / (times[1] - times[0])
        tr.stats.network = "NET"
        tr.stats.station = "STA"
        tr.stats.location = ""
        tr.stats.channel = "CH"

        st = Stream(traces=[tr])

        output = io.BytesIO()
        st.write(output, format="MSEED")
        output.seek(0)

        response = StreamingResponse(output, media_type="application/octet-stream")
        response.headers["Content-Disposition"] = (
            f"attachment; filename={file.filename.split('.')[0]}.mseed"
        )
        return response

    except Exception as e:
        return {"error": str(e)}
    finally:
        temp_file.close()
        os.remove(temp_file_path)


@app.post("/upload-mseed-to-png/")
async def upload_and_square(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

        st = read(temp_file_path)
        tr = st[0].copy()
        minfreq = 0.5
        tr.filter("highpass", freq=minfreq)
        tr_times = tr.times()
        tr_data = tr.data
        plt.figure(figsize=(12, 8))
        plt.plot(tr_times, tr_data, "b-", label="Señal Original")
        plt.title("Señal Original Filtrada con Paso Alto")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.legend()

        plt.tight_layout()
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png")
        img_buffer.seek(0)
        response = StreamingResponse(img_buffer, media_type="image/png")
        response.headers["Content-Disposition"] = (
            f"attachment; filename=señal_filtrada.png"
        )
        return response

    except Exception as e:
        return {"error": str(e)}

    finally:
        temp_file.close()


@app.post("/upload-mseed-to-json/")
async def upload_and_square(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name
        st = read(temp_file_path)
        tr = st[0].copy()
        tr_times = tr.times()
        tr_data = tr.data
        min_val = np.min(tr_data)
        max_val = np.max(tr_data)
        tr_data_minmax = 2 * (tr_data - min_val) / (max_val - min_val) - 1
        output = io.StringIO()
        output.write("{\n")
        output.write(f'  "time": {tr_times.tolist()},\n')
        output.write(f'  "normalized_data": {tr_data_minmax.tolist()}\n')
        output.write("}")
        output.seek(0)

        response = StreamingResponse(output, media_type="application/json")
        response.headers["Content-Disposition"] = (
            f"attachment; filename={file.filename.split('.')[0]}_normalized.json"
        )
        return response

    except Exception as e:
        return {"error": str(e)}
    finally:
        temp_file.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
