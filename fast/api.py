from fastapi import FastAPI, UploadFile, HTTPException
import pandas as pd

app = FastAPI()

df = None
df_remaining = None
df_success = None
df_fail = None

rand_index = None
current_phrase = None
current_hint = None
current_translation = None

current_translation_input = None

@app.post("/uploadfile/")
async def upload_csv(file: UploadFile):
    global df
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    try:
        df = pd.read_csv(file.file, usecols=["phrase","hint","translation"], delimiter=";")

    except Exception:
        return {"message": "There was an error uploading the file"}

    finally:
        file.file.close()

    return {"filename": file.filename,
            "content_type": file.content_type}


@app.get("/summary/")
async def summary():
    global df
    if df is None:
        raise HTTPException(status_code=404, detail="DataFrame not found. Please upload a CSV file first.")

    return {"summary": df.describe().to_dict()}


@app.get("/columns/")
async def columns():
    global df
    if df is None:
        raise HTTPException(status_code=404, detail="DataFrame not found. Please upload a CSV file first.")

    return {"columns": df.columns.tolist()}
