from fastapi import FastAPI, UploadFile, HTTPException
import pandas as pd

app = FastAPI()

df = None
df_remaining = None
df_success = None
df_fail = None

current_index = None
current_phrase = None
current_hint = None
current_translation = None

current_translation_input = None

@app.get("/")
def ping():
    return {"status": "ok"}


@app.post("/upload_csv/")
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

    return {
        "filename": file.filename,
        "row_count": df.shape[0],
        "column_names": df.columns.tolist()
    }


@app.get("/sample_random_row/")
def sample_random_row():
    if df is None:
        return {"message": "Please upload a csv file first"}
    else:
        sampled_row = df.sample()
        current_index = sampled_row.index
        current_phrase = sampled_row["phrase"].item()
        current_hint = sampled_row["hint"].item()
        current_translation = sampled_row["translation"].item()
        return sampled_row.to_dict("records")[0]
