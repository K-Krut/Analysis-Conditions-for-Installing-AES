import requests

from diploma_api.settings import RapidAPI_KEY

url = "https://meteostat.p.rapidapi.com/point/monthly"

querystring = {"lat": 50.330228, "lon": 26.239297, "start": "2020-01-01", "end": "2024-01-01"}

headers = {
    "X-RapidAPI-Key": "dc5637a942mshd7ef27900bfacc3p11b247jsna26aa27082fa",
    "X-RapidAPI-Host": RapidAPI_KEY
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
