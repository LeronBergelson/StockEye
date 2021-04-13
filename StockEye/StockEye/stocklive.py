import requests
import json


def live_price (ticker_symbol): 
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"

    querystring = {"symbol":ticker_symbol,"region":"CA"}

    headers = {
    'x-rapidapi-key': "e39748b442mshfcbeac829919eeep154368jsn26208687be77",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    return json.loads(response.text)["price"]["regularMarketPrice"]["fmt"]

print(live_price("AC.TO"))

