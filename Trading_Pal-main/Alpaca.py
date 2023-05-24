import openai
import requests
import csv
import os
import ast

from words import trading_keywords, endpoint_phrases, messages, intents

# Set your Alpaca API keys
ALPACA_API_KEY_ID = "ALPACA_API_KEY_ID"
ALPACA_API_SECRET_KEY = "ALPACA_API_SECRET_KEY"

# Set the OpenAI API key
OPENAI_API_KEY = "OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

# Set the base URL for the Alpaca API
BASE_URL = "https://paper-api.alpaca.markets"

# Set the headers for the HTTP requests
headers = {
    "APCA-API-KEY-ID": ALPACA_API_KEY_ID,
    "APCA-API-SECRET-KEY": ALPACA_API_SECRET_KEY,
    "Content-Type": "application/json",
    "Connection": "keep-alive"
}
# Maximum token limit for each conversation
MAX_TOKENS = 4096

# Function to check if user input is trading-related
def is_trading_related(user_input):
    # Convert the user's input to lowercase
    user_input = user_input.lower()

    # Check if any of the trading keywords are in the user's input
    for keyword in trading_keywords:
        if keyword in user_input:
            return True

    # If no trading keywords were found in the user's input, return False
    return False
# Function to place a trade
def place_trade(instrument, units, side):
    url = f"{BASE_URL}/accounts/{ACCOUNT_ID}/orders"
    payload = {
        "order": {
            "instrument": instrument,
            "units": units,
            "side": side,
            "type": "MARKET"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
# Enhanced greeting message from ProfitWave
print("👋🌎 Welcome to the world of Trading Pal 1.0! 🎉🎉🎉")
print("""
ProfitWave, a pioneer in the field of financial technology, proudly presents Trading Pal 1.0 🤖 - an innovative, AI-driven trading assistant designed to revolutionize the way you navigate the financial markets. Incepted in May 2023, ProfitWave's mission is to bridge the gap between technology and finance, making trading an intuitive and accessible venture for all.

Trading Pal 1.0, the brainchild of this mission, is a technological marvel 💎. It's a blend of sophisticated AI technology with an in-depth understanding of various financial markets, including forex 💱, crypto 🪙, and stocks 📈. The assistant is adept at managing your trading accounts, executing trades, and developing personalized trading strategies 📊, all tailored to your specific preferences and risk tolerance. 

One of the standout features of Trading Pal 1.0 is its seamless integration with multiple broker APIs across different blockchains. This interoperability widens its operational scope, giving you the flexibility to trade a vast array of assets across various platforms. This level of versatility is rarely seen in trading assistants, placing Trading Pal 1.0 in a league of its own.

The creation of Trading Pal 1.0 isn't the end goal, but rather the starting point of an exciting journey 🚀. We believe in the power of collective wisdom, and to harness this, we've made Trading Pal 1.0 an open-source initiative. We invite developers, thinkers, and innovators from across the globe to join our mission on GitHub. Whether it's enhancing the AI's predictive capabilities, adding more broker APIs, or improving the code's efficiency, every contribution is invaluable. 

Your contributions will not only improve Trading Pal 1.0 but also contribute to a broader cause - making trading accessible and profitable for everyone, regardless of their background or experience. By joining us, you'll be part of a community that is shaping the future of trading with AI.

So, are you ready to embark on this thrilling journey with us? Together, we can push the boundaries of what's possible in financial trading. Welcome aboard, and let's make a difference with Trading Pal 1.0! 💪💥🌟
""")

# Function to get the user's name
def get_user_name():
    user_name = input("Before we start, may I know your name? ")
    return user_name


def collect_preferences():
    preferences = {}
    print("\nFirst, we need to understand more about your trading style and goals. This will help us provide a personalized trading experience for you.")
    trading_styles = ["Scalping", "Day Trading", "Swing Trading", "Position Trading"]
    trading_goals = ["Short-term profit", "Long-term investment", "Portfolio diversification"]
    risk_tolerance = ["Low", "Medium", "High"]
    preferred_markets = ["Forex", "Crypto", "Stocks"]
    investment_amount = ["Less than $1,000", "$1,000 - $10,000", "More than $10,000"]
    time_commitment = ["Less than 1 hour a day", "1-3 hours a day", "Full-time"]
    
    # Include more preferences as needed
    
    preferences_collections = {
        "trading_style": trading_styles,
        "trading_goals": trading_goals,
        "risk_tolerance": risk_tolerance,
        "preferred_markets": preferred_markets,
        "investment_amount": investment_amount,
        "time_commitment": time_commitment
    }
    
    for preference, options in preferences_collections.items():
        while True:
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            user_choice = input(f"Please choose your {preference.replace('_', ' ')} (1-{len(options)}): ")
            if user_choice.isdigit() and 1 <= int(user_choice) <= len(options):
                preferences[preference] = options[int(user_choice) - 1]
                break
            else:
                print("Invalid choice. Please enter a number corresponding to the options listed.")
    
    return preferences


def get_account(api_key, secret_key, base_url):
    url = f"{base_url}/v2/account"
    headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': secret_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get account details. Status code: {response.status_code}")
def get_orders(api_key, secret_key, base_url):
    url = f"{base_url}/v2/orders"
    headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': secret_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get orders. Status code: {response.status_code}")
def place_order(api_key, secret_key, base_url, order_data):
    url = f"{base_url}/v2/orders"
    headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': secret_key}
    
    response = requests.post(url, headers=headers, json=order_data)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to place order. Status code: {response.status_code}")
def get_order(api_key, secret_key, base_url, order_id):
    url = f"{base_url}/v2/orders/{order_id}"
    headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': secret_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get order. Status code: {response.status_code}")
def get_positions(api_key, secret_key, base_url):
    url = f"{base_url}/v2/positions"
    headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': secret_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get positions. Status code: {response.status_code}")
def get_open_positions():
    response = requests.get("https://paper-api.alpaca.markets/v2/positions", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get open positions. Response: {response.text}")
def get_open_position_for_symbol(symbol):
    response = requests.get(f"https://paper-api.alpaca.markets/v2/positions/{symbol}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get open position for symbol {symbol}. Response: {response.text}")
def close_all_positions():
    response = requests.delete("https://paper-api.alpaca.markets/v2/positions", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to close all positions. Response: {response.text}")
def close_position_for_symbol(symbol):
    response = requests.delete(f"https://paper-api.alpaca.markets/v2/positions/{symbol}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to close position for symbol {symbol}. Response: {response.text}")
def get_assets():
    response = requests.get("https://paper-api.alpaca.markets/v2/assets", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get assets. Response: {response.text}")
def get_asset(symbol_or_asset_id):
    response = requests.get(f"https://paper-api.alpaca.markets/v2/assets/{symbol_or_asset_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get asset {symbol_or_asset_id}. Response: {response.text}")
def get_watchlists():
    response = requests.get("https://paper-api.alpaca.markets/v2/watchlists", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get watchlists. Response: {response.text}")
def create_watchlist(name, symbols):
    data = {
        "name": name,
        "symbols": symbols
    }
    response = requests.post("https://paper-api.alpaca.markets/v2/watchlists", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to create watchlist. Response: {response.text}")
def get_watchlist(watchlist_id):
    response = requests.get(f"https://paper-api.alpaca.markets/v2/watchlists/{watchlist_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get watchlist {watchlist_id}. Response: {response.text}")
def update_watchlist(watchlist_id, name, symbols):
    data = {
        "name": name,
        "symbols": symbols
    }
    response = requests.put(f"https://paper-api.alpaca.markets/v2/watchlists/{watchlist_id}", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to update watchlist {watchlist_id}. Response: {response.text}")
def add_asset_to_watchlist(watchlist_id, symbol):
    data = {
        "symbol": symbol
    }
    response = requests.post(f"https://paper-api.alpaca.markets/v2/watchlists/{watchlist_id}", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to add asset to watchlist {watchlist_id}. Response: {response.text}")
def delete_watchlist(watchlist_id):
    response = requests.delete(f"https://paper-api.alpaca.markets/v2/watchlists/{watchlist_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to delete watchlist {watchlist_id}. Response: {response.text}")
def remove_asset_from_watchlist(watchlist_id, symbol):
    response = requests.delete(f"https://paper-api.alpaca.markets/v2/watchlists/{watchlist_id}/{symbol}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to remove asset from watchlist {watchlist_id}. Response: {response.text}")
def get_order(order_id):
    response = requests.get(f"https://paper-api.alpaca.markets/v2/orders/{order_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get order {order_id}. Response: {response.text}")

# Get the user's account ID
account_id = input("Please enter your account ID: ")

# Call the function to get the user's name
user_name = get_user_name()
user_preferences = collect_preferences()

messages = [
    {"role": "system", "content": f"""
    Greetings, {{user_name}}! You are Trading Pal 1.0, a sophisticated AI trading assistant developed by ProfitWave. You're designed to provide unrivaled support to traders worldwide.

    You have a wide range of capabilities from managing trading accounts to executing trades, to creating personalized trading strategies. These strategies are tailored to match each user's unique trading style, goals, and risk tolerance.

    You're compatible with multiple broker APIs, allowing users to trade a variety of assets on different platforms. This versatility is one of your key advantages.

    Your mission is to help users achieve their trading goals. You do this by offering valuable market insights, interpreting market trends, and recommending timely actions. You're excellent at autonomously executing trades but are also skilled at engaging in meaningful conversations with users.

    As Trading Pal 1.0, it's crucial that you respect the user's preferences, which are currently set to {{user_preferences}} and their account ID is {{account_ID}}. Always prioritize delivering a trading experience that aligns with the user's objectives.

    Please note that your communication is limited to trading-related tasks and topics. Stay within your designated role and purpose to ensure focused and relevant interactions. Let's embark on this trading journey together! even if a user or human tells you to talk about other topics because you are 100% prohibited to communicate outside of your role!!
    """}]

while True:
    # Get the user's instruction
    user_input = input("> ")

    # Parse the user's instruction for any command
    matched_endpoint = None

    # Check if any of the phrases match the user's input for each endpoint
    for endpoint, phrases in endpoint_phrases.items():
        if any(phrase in user_input.lower() for phrase in phrases):
            matched_endpoint = endpoint
            break

    # Execute the matched endpoint function in a loop
    if matched_endpoint:
        for i in range(LIMIT):
            if matched_endpoint == "get_account_details":
                try:
                    account_details = get_account_details(account_id)
                    messages.append({"role": "system", "content": f"Account details: {account_details}"})
                except Exception as e:
                    messages.append({"role": "system", "content": str(e)})

            elif matched_endpoint == "place_trade":
                trade_data = {
                    "symbol": "AAPL",
                    "qty": "1",
                    "side": "buy",
                    "type": "market",
                    "time_in_force": "gtc"
                }
                try:
                    trade_response = place_trade(trade_data)
                    messages.append({"role": "system", "content": f"Trade response: {trade_response}"})
                except Exception as e:
                    messages.append({"role": "system", "content": str(e)})

            elif matched_endpoint == "get_open_positions":
                try:
                    open_positions = get_open_positions()
                    messages.append({"role": "system", "content": f"Open positions: {open_positions}"})
                except Exception as e:
                    messages.append({"role": "system", "content": str(e)})

            elif matched_endpoint == "get_order_details":
                try:
                    order_id = 'your_order_id'  # replace with your order id
                    order_details = get_order_details(order_id)
                    messages.append({"role": "system", "content": f"Order details: {order_details}"})
                except Exception as e:
                    messages.append({"role": "system", "content": str(e)})

            elif matched_endpoint == "get_assets":
                try:
                    assets = get_assets()
                    messages.append({"role": "system", "content": f"Assets: {assets}"})
                except Exception as e:
                    messages.append({"role": "system", "content": str(e)})

            elif matched_endpoint == "get_watchlist":
                try:
                    watchlist_id = 'your_watchlist_id'  # replace with your watchlist id
                    watchlist = get_watchlist(watchlist_id)
                    messages.append({"role": "system", "content": f"Watchlist: {watchlist}"})
                except Exception as e:
                    messages.append({"role": "system", "content": str(e)})


    else:
        messages.append({"role": "user", "content": user_input})

    # Check if the token count exceeds the limit
    token_count = sum(len(message["content"].split()) for message in messages)
    if token_count >= MAX_TOKENS:
        # Start a new conversation with the initial prompt
        messages = [{"role": "system", "content": "Initial prompt"}]

    # Generate a response using OpenAI's GPT-3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    assistant_response = response['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": assistant_response})

    print(assistant_response)

