
from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingStream
import csv
from oandapyV20.exceptions import StreamTerminated

access_token = "620effdf7830ee7ca93f668147bbd71c-fb7b8385d044e4274a5bed321d34fcad"
account_id = "101-001-25239678-001"

api = API(access_token=access_token, environment="practice")

params = {
    "instruments": "EUR_USD"
}

r = PricingStream(accountID=account_id, params=params)

def save_to_csv(data):
    with open('streaming_data.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow(data.values())

try:
    rv = api.request(r)
    for ticks in rv:
        if ticks['type'] != 'HEARTBEAT':
            save_to_csv(ticks)
except StreamTerminated as e:
    print(e)