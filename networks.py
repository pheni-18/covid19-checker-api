from constants import OPEN_DATA_URL

import json
import requests


class OpenDataClient:
    _url = OPEN_DATA_URL + 'Covid19JapanAll'

    @classmethod
    def get_total(cls, date: str) -> list:
        res = requests.get(f'{cls._url}?date={date}')
        if not res.status_code == requests.codes.ok:
            raise Exception

        dict_ = json.loads(res.text)

        return dict_['itemList']
