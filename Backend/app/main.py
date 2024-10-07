import os
import tempfile
import numpy as np
from obspy import read
from obspy.signal.trigger import classic_sta_lta, trigger_onset
from scipy.signal import medfilt
import noisereduce as nr
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
from obspy import read
import io
import matplotlib.pyplot as plt
import re
from dotenv import load_dotenv
import google.generativeai as genai

app = FastAPI()
base_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(base_dir, "results")
print(results_dir)

app.mount("/results", StaticFiles(directory=results_dir), name="results")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def process_data_to_json(times, data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data_minmax = 2 * (data - min_val) / (max_val - min_val) - 1
    output = io.StringIO()
    output.write("{\n")
    output.write(f'  "time": {times.tolist()},\n')
    output.write(f'  "normalized_data": {normalized_data_minmax.tolist()}\n')
    output.write("}")
    output.seek(0)

    return output


def deserialize_response(response_text):
    pattern = r"'sta':\s*(\d+),\s*'lta':\s*(\d+),\s*'confirmation':\s*'(yes|no)'"
    match = re.search(pattern, response_text)

    if match:
        sta = int(match.group(1))
        lta = int(match.group(2))
        confirmation = match.group(3)
        return sta, lta, confirmation
    else:
        raise ValueError("Could not deserialize the response. Invalid format.")


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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload-mseed-or-csv-to-json/")
async def upload_mseed_or_csv_to_json(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension == "csv":
            data = np.genfromtxt(temp_file_path, delimiter=",", skip_header=1)
            times = data[:, 0]
            normalized_data = data[:, 1]
            output = process_data_to_json(times, normalized_data)

        elif file_extension == "mseed":
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


@app.post("/detect-events/")
async def detect_events(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with temp_file:
            shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name
        results_dir = "results"
        filename = os.path.splitext(file.filename)[0]
        file_results_dir = os.path.join(results_dir, filename)

        if os.path.exists(file_results_dir):
            return FileResponse(
                os.path.join(file_results_dir, "event_results", "event_results.svg")
            )

        os.makedirs(file_results_dir, exist_ok=True)
        median_dir = os.path.join(file_results_dir, "median")
        characteristic_dir = os.path.join(file_results_dir, "characteristic")
        event_results_dir = os.path.join(file_results_dir, "event_results")

        os.makedirs(median_dir, exist_ok=True)
        os.makedirs(characteristic_dir, exist_ok=True)
        os.makedirs(event_results_dir, exist_ok=True)

        st = read(temp_file_path)
        tr = st[0].copy()

        minfreq = 0.5
        tr.filter("highpass", freq=minfreq)

        tr_times = tr.times()
        tr_data = tr.data

        min_val = np.min(tr_data)
        max_val = np.max(tr_data)
        tr_data_minmax = 2 * (tr_data - min_val) / (max_val - min_val) - 1

        tr_data_median_filtered = medfilt(tr_data_minmax, kernel_size=5)

        plt.figure(figsize=(12, 8))

        plt.subplot(3, 1, 1)
        plt.plot(tr_times, tr_data_median_filtered, "r-", label="Median Filtered")
        plt.title("Signal Filtered with Median Filter")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.savefig(os.path.join(median_dir, "median.svg"), format="svg")
        plt.close()

        sample_rate = 1 / (tr_times[1] - tr_times[0])
        signal_cleaned = nr.reduce_noise(
            y=tr_data_median_filtered, sr=sample_rate, time_mask_smooth_ms=40000
        )

        confirmation = "no"
        i = 0

        df = tr.stats.sampling_rate

        while confirmation != "yes":
            if i == 0:
                sta_len = 60
                lta_len = 1200
            else:
                sta_len, lta_len, confirmation = deserialize_response(response.text)

            cft = classic_sta_lta(signal_cleaned, int(sta_len * df), int(lta_len * df))

            min_duration = 420
            min_duration_samples = int(min_duration * df)

            fig, ax = plt.subplots(1, 1, figsize=(12, 3))
            ax.plot(tr_times, cft)
            ax.set_xlim([min(tr_times), max(tr_times)])
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Characteristic function")
            plt.savefig(
                os.path.join(characteristic_dir, f"characteristic-{i}.png"),
                format="png",
            )
            plt.savefig(
                os.path.join(characteristic_dir, f"characteristic-{i}.svg"),
                format="svg",
            )
            plt.close()

            response = model.generate_content(
                [
                    upload_to_gemini(
                        os.path.join(characteristic_dir, f"characteristic-{i}.png"),
                        mime_type="image/png",
                    ),
                    "The graph is improving, but we need to optimize it further. Please suggest a new value for the STA and LTA windows to obtain a better graph. Respond **only** in the following format: {'sta': <new_sta_value>, 'lta': <new_lta_value>, 'confirmation': <yes or no>}. Make sure the response contains only values in this format.",
                ]
            )

            i += 1

        thresholds = [
            {"on": 12, "off": 1},
            {"on": 10, "off": 1},
            {"on": 6, "off": 1},
            {"on": 5, "off": 1},
            {"on": 4, "off": 1},
            {"on": 1.8, "off": 1},
            {"on": 1.5, "off": 1},
            {"on": 1.1, "off": 1},
        ]

        filtered_on_off = []
        min_duration_samples = 420
        detected_events = set()

        for idx, thr in enumerate(thresholds):
            thr_on = thr["on"]
            thr_off = thr["off"]

            on_off = np.array(trigger_onset(cft, thr_on, thr_off))

            temp_filtered = []
            for triggers in on_off:
                if (triggers[1] - triggers[0]) >= min_duration_samples:
                    event_range = range(triggers[0], triggers[1] + 1)
                    if not any(time in detected_events for time in event_range):
                        temp_filtered.append(triggers)
                        detected_events.update(event_range)

            temp_filtered = np.array(temp_filtered)
            if len(temp_filtered) > 0:
                filtered_on_off.extend(temp_filtered.tolist())

        if len(filtered_on_off) > 0:
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

            plt.title(f"Results with {len(filtered_on_off)} detected events")
            plt.savefig(
                os.path.join(event_results_dir, "event_results.svg"), format="svg"
            )
            plt.close()
        else:
            print(
                "No events meeting the minimum duration were found at any thresholds."
            )

        return FileResponse(os.path.join(event_results_dir, "event_results.svg"))

    finally:
        temp_file.close()


@app.get("/list-images/")
async def list_images():
    results_dir = "results"
    image_structure = {}
    base_url = "http://localhost:8000"

    if os.path.exists(results_dir):
        for root, dirs, files in os.walk(results_dir):
            relative_root = os.path.relpath(root, start=results_dir).replace(
                os.sep, "/"
            )
            print(relative_root)
            if relative_root not in image_structure:
                image_structure[relative_root] = []

            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg", ".svg")):
                    image_url = f"{base_url}/results/{relative_root}/{file}"
                    image_structure[relative_root].append(image_url)
    return JSONResponse(content=image_structure)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
