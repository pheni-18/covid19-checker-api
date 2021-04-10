from networks import OpenDataClient

import datetime


class CovidService:
    _client = OpenDataClient()

    @classmethod
    def get_all_by_date(cls, date: datetime.date) -> list:
        total1 = cls._client.get_total(date)

        next_date = date - datetime.timedelta(days=1)
        total2 = cls._client.get_total(next_date)

        prefectures = []
        for p1, p2 in zip(total1, total2):
            if not p1['name_jp'] == p2['name_jp']:
                raise Exception

            diff = int(p1['npatients']) - int(p2['npatients'])
            prefectures.append({
                'name': p1['name_jp'],
                'date': date,
                'count': diff
            })

        return prefectures
