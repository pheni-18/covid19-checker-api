from fastapi import FastAPI, HTTPException
from services import CovidService

import datetime

app = FastAPI()


class ValidationError(Exception):
    pass


def str8_to_date(date: str) -> datetime.date:
    if len(date) != 8:
        raise ValidationError()

    try:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        return datetime.date(year, month, day)
    except ValueError as e:
        raise ValidationError()


@app.get("/all")
def get_all(date: str):
    try:
        d = str8_to_date(date)
        res = CovidService.get_all_by_date(d)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="'date' is invalid")
    except Exception as e:
        raise HTTPException(status_code=500, detail="API error")

    return res
