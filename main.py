from fastapi import FastAPI, HTTPException
from services import CovidService

app = FastAPI()


@app.get("/all")
def get_all(date: str):
    try:
        res = CovidService.get_all_by_date(date)
    except Exception as e:
        raise HTTPException(status_code=500, detail="API error")

    return res
