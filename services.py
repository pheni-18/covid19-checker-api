from networks import OpenDataClient

import datetime


class CovidService:
    _client = OpenDataClient()

    @classmethod
    def get_all_by_date(cls, date: str) -> list:
        total1 = cls._client.get_total(date)

        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])
        d1 = datetime.date(year, month, day)
        d2 = d1 - datetime.timedelta(days=1)

        total2 = cls._client.get_total(d2.strftime('%Y%m%d'))

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
