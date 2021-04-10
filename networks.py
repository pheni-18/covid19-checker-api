from constants import OPEN_DATA_URL
from datetime import date

import json
import requests


class OpenDataClient:
    _url = OPEN_DATA_URL + 'Covid19JapanAll'

    @classmethod
    def get_total(cls, date_: date) -> list:
        d = date_.strftime('%Y%m%d')
        res = requests.get(f'{cls._url}?date={d}')
        if not res.status_code == requests.codes.ok:
            raise Exception

        dict_ = json.loads(res.text)

        return dict_['itemList']
