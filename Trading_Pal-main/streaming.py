from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingStream
import csv
from oandapyV20.exceptions import StreamTerminatedError



access_token = "620effdf7830ee7ca93f668147bbd71c-fb7b8385d044e4274a5bed321d34fcad"
account_id = "101-001-25239678-001"

api = API(access_token=access_token, environment="practice")

params = {
    "instruments": "EUR_USD"
}

r = PricingStream(accountID=account_id, params=params)

def save_to_csv(data):
    try:
        with open('streaming_data.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    except Exception as e:
        print(f"Error saving data to CSV file: {e}")

def process_data(ticks):
    try:
        # Extract relevant information from the ticks
        time = ticks['time']
        volume = ticks.get('volume', 0)  # Use 0 as the default value if 'volume' key is not present
        bid_price = float(ticks['bids'][0]['price'])
        ask_price = float(ticks['asks'][0]['price'])
        # Calculate other necessary values from the extracted information
        open_price = (bid_price + ask_price) / 2
        high_price = max(bid_price, ask_price)
        low_price = min(bid_price, ask_price)
        close_price = (bid_price + ask_price) / 2

        # Format the processed data
        processed_data = [time, volume, open_price, high_price, low_price, close_price]

        # Perform actions with the processed data (e.g., save to CSV file)
        save_to_csv(processed_data)
    except Exception as e:
        print(f"Error processing data: {e}")

try:
    rv = api.request(r)
    for ticks in rv:
        if ticks['type'] != 'HEARTBEAT':
            process_data(ticks)
except StreamTerminatedError as e:
    print(e)
except Exception as e:
    print(f"Error requesting data from OANDA API: {e}")