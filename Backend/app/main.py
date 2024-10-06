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
import re
from dotenv import load_dotenv
import google.generativeai as genai

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


def process_data_to_json(times, data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data_minmax = 2 * (data - min_val) / (max_val - min_val) - 1

    # Crear JSON a partir de los datos
    output = io.StringIO()
    output.write("{\n")
    output.write(f'  "time": {times.tolist()},\n')
    output.write(f'  "normalized_data": {normalized_data_minmax.tolist()}\n')
    output.write("}")
    output.seek(0)

    return output


@app.post("/upload-csv-to-mseed/")
async def upload_csv_to_mseed(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

        data = np.genfromtxt(temp_file_path, delimiter=",", skip_header=1)
        times = data[:, 0]
        normalized_data = data[:, 1]

        # Normalización y generación de MSEED
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


@app.post("/upload-mseed-to-json/")
async def upload_mseed_to_json(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

        st = read(temp_file_path)
        tr = st[0].copy()
        tr_times = tr.times()
        tr_data = tr.data

        output = process_data_to_json(tr_times, tr_data)

        response = StreamingResponse(output, media_type="application/json")
        response.headers["Content-Disposition"] = (
            f"attachment; filename={file.filename.split('.')[0]}_normalized.json"
        )
        return response

    except Exception as e:
        return {"error": str(e)}
    finally:
        temp_file.close()
        os.remove(temp_file_path)


@app.post("/upload-mseed-or-csv-to-json/")
async def upload_mseed_or_csv_to_json(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

        # Detectar el tipo de archivo basado en la extensión
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension == "csv":
            # Procesar como CSV
            data = np.genfromtxt(temp_file_path, delimiter=",", skip_header=1)
            times = data[:, 0]
            normalized_data = data[:, 1]
            output = process_data_to_json(times, normalized_data)

        elif file_extension == "mseed":
            # Procesar como MSEED
            st = read(temp_file_path)
            tr = st[0].copy()
            tr_times = tr.times()
            tr_data = tr.data
            output = process_data_to_json(tr_times, tr_data)

        else:
            return {
                "error": "Unsupported file format. Please upload CSV or MSEED files."
            }

        response = StreamingResponse(output, media_type="application/json")
        response.headers["Content-Disposition"] = (
            f"attachment; filename={file.filename.split('.')[0]}_normalized.json"
        )
        return response

    except Exception as e:
        return {"error": str(e)}
    finally:
        temp_file.close()
        os.remove(temp_file_path)


def deserializar_respuesta(respuesta_texto):
    # Expresión regular para capturar valores de 'sta', 'lta' y 'confirmation'
    patron = r"'sta':\s*(\d+),\s*'lta':\s*(\d+),\s*'confirmation':\s*'(yes|no)'"

    # Buscar el patrón en el texto de respuesta
    match = re.search(patron, respuesta_texto)

    if match:
        sta = int(match.group(1))  # Extraer y convertir 'sta' a entero
        lta = int(match.group(2))  # Extraer y convertir 'lta' a entero
        confirmation = match.group(3)  # Extraer 'confirmation' (yes o no)
        return sta, lta, confirmation
    else:
        raise ValueError("No se pudo deserializar la respuesta. Formato inválido.")


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)


def upload_to_gemini(path, mime_type=None):
    load_dotenv()

    gemini_api_key = os.getenv("API_KEY")
    genai.configure(api_key=gemini_api_key)

    file = genai.upload_file(path, mime_type=mime_type)
    return file


@app.post("/detect-events/")
async def detect_events(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

        st = read(temp_file_path)
        tr = st[0].copy()

        # Apply a highpass filter
        minfreq = 0.5
        tr.filter("highpass", freq=minfreq)

        # Obtain filtered trace data
        tr_times = tr.times()
        tr_data = tr.data

        # Min-Max normalization
        min_val = np.min(tr_data)
        max_val = np.max(tr_data)
        tr_data_minmax = (
            2 * (tr_data - min_val) / (max_val - min_val) - 1
        )  # Escalado entre -1 y 1

        # 1. Apply a Median Filter
        tr_data_median_filtered = medfilt(tr_data_minmax, kernel_size=5)

        # Visualize the signals
        plt.figure(figsize=(12, 8))

        # Filtered Signal with Median
        plt.subplot(3, 1, 1)
        plt.plot(tr_times, tr_data_median_filtered, "r-", label="Filtrada con Mediana")
        plt.title("Señal Filtrada con Filtro de Mediana")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Amplitud")
        plt.savefig("mediana.png")
        plt.close()

        # 2. Apply Noise Reduction
        sample_rate = 1 / (tr_times[1] - tr_times[0])  # Calculate sampling rate
        signal_cleaned = nr.reduce_noise(
            y=tr_data_median_filtered, sr=sample_rate, time_mask_smooth_ms=40000
        )

        confirmation = (
            "no"  # You want to set confirmation to "no" to begin the while loop
        )
        i = 0

        # Sampling frequency of the trace
        df = tr.stats.sampling_rate

        while confirmation != "yes":
            if i == 0:
                # Default STA/LTA window lengths
                sta_len = 60  # Short-term window in seconds
                lta_len = 1200  # Long-term window in seconds
            else:
                # Use the updated window lengths from the user response
                sta_len, lta_len, confirmation = deserializar_respuesta(response.text)

            # Run Obspy's STA/LTA to obtain a characteristic function
            cft = classic_sta_lta(signal_cleaned, int(sta_len * df), int(lta_len * df))

            # Define the minimum event duration (in seconds)
            min_duration = 420  # Adjust as per requirements
            # Convert minimum duration to samples
            min_duration_samples = int(min_duration * df)

            # Plot the characteristic function
            fig, ax = plt.subplots(1, 1, figsize=(12, 3))
            ax.plot(tr_times, cft)
            ax.set_xlim([min(tr_times), max(tr_times)])
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Characteristic function")
            plt.savefig("caracteristica.png")
            plt.close()

            response = model.generate_content(
                [
                    upload_to_gemini("caracteristica.png", mime_type="image/png"),
                    "The graph is improving, but we need to optimize it further. Please suggest a new value for the STA and LTA windows to obtain a better graph. Respond **only** in the following format: {'sta': <new_sta_value>, 'lta': <new_lta_value>, 'confirmation': <yes or no>}. Make sure the response contains only values in this format.",
                ]
            )

            i += 1  # Increment the loop counter

        # Define thresholds for event detection
        thresholds = [
            {"on": 12, "off": 1},  # Umbrales para el primer evento
            {"on": 10, "off": 1},  # Umbrales para el segundo evento
            {"on": 6, "off": 1},  # Umbrales para el tercer evento
            {"on": 5, "off": 1},  # Umbrales para el cuarto evento
            {"on": 4, "off": 1},  # Umbrales para el quinto evento
            {"on": 1.8, "off": 1},  # Umbrales para el sexto evento
            {"on": 1.5, "off": 1},  # Umbrales para el séptimo evento
            {"on": 1.1, "off": 1},  # Umbrales para el octavo evento
        ]

        filtered_on_off = []  # Inicializa la lista que almacenará los eventos filtrados
        min_duration_samples = 420  # Ejemplo de duración mínima para un evento
        detected_events = (
            set()
        )  # Inicializar un conjunto para almacenar los tiempos de los triggers ya detectados

        # Mientras que no se encuentren eventos válidos y haya más umbrales que probar
        for idx, thr in enumerate(thresholds):
            thr_on = thr["on"]  # Obtiene el umbral de activación actual
            thr_off = thr["off"]  # Obtiene el umbral de desactivación actual

            # Obtener los triggers usando los umbrales actuales
            on_off = np.array(trigger_onset(cft, thr_on, thr_off))

            # Filtrar los eventos que duren menos que el tiempo mínimo
            temp_filtered = []
            for triggers in on_off:
                if (triggers[1] - triggers[0]) >= min_duration_samples:
                    event_range = range(triggers[0], triggers[1] + 1)
                    if not any(time in detected_events for time in event_range):
                        temp_filtered.append(triggers)
                        detected_events.update(
                            event_range
                        )  # Agregar el rango del evento detectado

            temp_filtered = np.array(temp_filtered)
            if len(temp_filtered) > 0:
                filtered_on_off.extend(temp_filtered.tolist())

        if len(filtered_on_off) > 0:
            # Graficar los triggers on y off (solo los filtrados)
            fig, ax = plt.subplots(1, 1, figsize=(12, 3))
            for i, triggers in enumerate(filtered_on_off):
                ax.axvline(
                    x=tr_times[triggers[0]],
                    color="red",
                    label="Trig. On" if i == 0 else "",
                )
                ax.axvline(
                    x=tr_times[triggers[1]],
                    color="purple",
                    label="Trig. Off" if i == 0 else "",
                )

            ax.plot(tr_times, tr_data)
            ax.set_xlim([min(tr_times), max(tr_times)])

            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            ax.legend(by_label.values(), by_label.keys())

            plt.title(f"Resultados con {len(filtered_on_off)} eventos detectados")

            plt.savefig("resultados_eventos.svg", format="svg")
            plt.close()
        else:
            print(
                "No se encontraron eventos que cumplan la duración mínima en ninguno de los umbrales."
            )
        return FileResponse("resultados_eventos.svg")

    finally:
        temp_file.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
