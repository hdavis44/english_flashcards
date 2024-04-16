import os
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
import pandas as pd

app = FastAPI()
# app.mount("/data", StaticFiles(directory=os.path.abspath("data")), name="data")

app.df = None
app.df_remaining = None
app.df_success = None
app.df_fail = None

app.pool = None
app.pool_index = None

app.current_index = None
app.current_phrase = None
app.current_hint = None
app.current_translation = None

app.current_translation_input = None

@app.get("/")
def ping():
    return {"status": "ok"}


@app.post("/upload_csv/")
async def upload_csv(file: UploadFile):
    if not (file.filename.endswith('.csv') and file.content_type == 'text/csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    try:
        app.df = pd.read_csv(file.file, usecols=["phrase","hint","translation"], delimiter=";")

    except Exception:
        return {"Message": "There was an error uploading the file."}

    finally:
        file.file.close()

    return {
        "content_type": file.content_type,
        "filename": file.filename,
        "row_count": app.df.shape[0],
        "column_names": app.df.columns.tolist()
    }


@app.get("/sample_twenty_rows/")
def sample_twenty_rows():
    if app.df is None:
        return {"Message": "Please upload a csv file first."}
    else:
        app.pool = app.df.sample(20)
        app.pool_index = app.pool.index
        return app.pool.to_dict("index")


@app.get("/sample_random_row/")
def sample_random_row():
    if app.df is None:
        return {"Message": "Please upload a csv file first."}
    else:
        app.sampled_row = app.df.sample()
        app.current_index = app.sampled_row.index
        app.current_phrase = app.sampled_row["phrase"].item()
        app.current_hint = app.sampled_row["hint"].item()
        app.current_translation = app.sampled_row["translation"].item()
        return app.sampled_row.to_dict("records")[0]
