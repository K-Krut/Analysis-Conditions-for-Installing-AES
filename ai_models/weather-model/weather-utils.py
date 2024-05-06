from builtins import print

import requests

from diploma_api.settings import RapidAPI_KEY

url = "https://meteostat.p.rapidapi.com/point/monthly"

querystring = {"lat": 50.330228, "lon": 26.239297, "start": "2023-01-01", "end": "2024-01-01"}

headers = {
    "X-RapidAPI-Key": RapidAPI_KEY,
    "X-RapidAPI-Host": "meteostat.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())



##################################################################################################
