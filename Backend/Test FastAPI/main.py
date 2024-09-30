from fastapi import FastAPI, UploadFile, File
import csv, io
from starlette.responses import StreamingResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Test: squared numbers"}

@app.post("/upload-and-square/")
async def upload_and_square(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return {"error": "Invalid file format. Please upload a CSV file."}

    contents = await file.read()
    decoded = contents.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(decoded))
    
    header = next(csv_reader)
    if "number" not in header:
        return {"error": "The CSV must contain a 'number' column."}

    number_index = header.index("number")

    squared_data = []
    squared_data.append(header)

    for row in csv_reader:
        try:
            number = int(row[number_index])
            row[number_index] = number ** 2
        except ValueError:
            return {"error": f"Invalid number value in row: {row}"}
        squared_data.append(row)

    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerows(squared_data)
    output.seek(0)

    response = StreamingResponse(output, media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={file.filename.split('.')[0]}_squared.csv"
    return response