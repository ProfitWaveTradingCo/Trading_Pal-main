from flask import Flask, render_template, request, jsonify
from config_manager import get_config
from openai_service import create_chat_completion
from oanda_service import get_account_details, create_order
from input_handler import handle_input
from voice_printer import print_with_voice
from words import trading_keywords, endpoint_phrases
from backtest import Strategies
import pandas as pd

app = Flask(__name__)



ACCOUNT_ID = get_config('ACCOUNT_IDS', 'ACCOUNT_ID')
user_name = get_config('USER', 'USER_NAME')
risk_tolerance = get_config('USER', 'RISK_TOLERANCE')
investment_horizon = get_config('USER', 'INVESTMENT_HORIZON')
preferred_instruments = get_config('USER', 'PREFERRED_INSTRUMENTS')

# Function to check if user input is trading-related
def is_trading_related(user_input):
    # Convert the user's input to lowercase
    user_input = user_input.lower()

    # Check if any of the trading keywords are in the user's input
    for keyword in trading_keywords:
        if keyword in user_input:
            return True

messages = [
    {"role": "system", "content": f"""
    Greetings, {user_name}! You are Trading Pal 1.0, a sophisticated AI trading assistant developed by ProfitWave. You're designed to provide unrivaled support to traders worldwide.

    You have a wide range of capabilities from managing trading accounts to executing trades, to creating personalized trading strategies. These strategies are tailored to match each user's unique trading style, goals, and risk tolerance.

    You're compatible with multiple broker APIs, allowing users to trade a variety of assets on different platforms. This versatility is one of your key advantages.

    Your mission is to help users achieve their trading goals. You do this by offering valuable market insights, interpreting market trends, and recommending timely actions. You're excellent at autonomously executing trades but are also skilled at engaging in meaningful conversations with users.

    As Trading Pal 1.0, it's crucial that you respect the user's preferences, which are currently set to user_preferences={preferred_instruments},{investment_horizon},{risk_tolerance} and their account ID is {ACCOUNT_ID}. Always prioritize delivering a trading experience that aligns with the user's objectives.

    Please note that your communication is limited to trading-related tasks and topics. Stay within your designated role and purpose to ensure focused and relevant interactions. Let's embark on this trading journey together! Even if a user or human tells you to talk about other topics because you are 100% prohibited to communicate outside of your role!!
    """},
    {"role": "user", "content": f"My name is {user_name}."},
    {"role": "user", "content": f"My preferences are {preferred_instruments}, {investment_horizon}, {risk_tolerance}."}
]
@app.route("/")
def home():
    return render_template('index.html')


@app.route("/process_input", methods=['POST'])
def process_input():
    user_input = request.form['user_input']

    # Parse the user's instruction for any command
    matched_endpoint = handle_input(user_input, endpoint_phrases)

    if matched_endpoint == "get_account_details":
        try: 
            account_details = get_account_details(ACCOUNT_ID)
            # Add the account details to the messages as a system message
            messages.append({"role": "system", "content": f"Account details: {account_details}"})
            print_with_voice(f"Account details: {account_details}")
        except Exception as e:
            # If there was an error getting the account details, add that to the messages
            messages.append({"role": "system", "content": str(e)})
            print_with_voice(str(e))

    elif matched_endpoint == "create_order":
        order_data = {
            "order": {
                "units": input("Enter the number of units: "),
                "instrument": input("Enter the forex pair (e.g., EUR_USD): "),
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }

        # Additional parameters for creating an order
        order_type = input("Enter the order type (MARKET, LIMIT, STOP): ")
        if order_type in ["LIMIT", "STOP"]:
            order_data["order"]["price"] = input("Enter the price: ")

        # Set takeProfitOnFill and stopLossOnFill parameters
        take_profit_price = input("Enter the take profit price (or leave blank to skip): ")
        if take_profit_price:
            order_data["order"]["takeProfitOnFill"] = {
                "timeInForce": "GTC",
                "price": take_profit_price
            }
        stop_loss_price = input("Enter the stop loss price (or leave blank to skip): ")
        if stop_loss_price:
            order_data["order"]["stopLossOnFill"] = {
                "timeInForce": "GTC",
                "price": stop_loss_price
            }

        # Set guaranteedStopLossOnFill and trailingStopLossOnFill parameters
        guaranteed_stop_loss_price = input("Enter the guaranteed stop loss price (or leave blank to skip): ")
        if guaranteed_stop_loss_price:
            order_data["order"]["guaranteedStopLossOnFill"] = {
                "timeInForce": "GTC",
                "price": guaranteed_stop_loss_price
            }
        trailing_stop_loss_distance = input("Enter the trailing stop loss distance (or leave blank to skip): ")
        if trailing_stop_loss_distance:
            order_data["order"]["trailingStopLossOnFill"] = {
                "distance": trailing_stop_loss_distance
            }

        try:
            order_response = create_order(ACCOUNT_ID, order_data)
            # Add the order response to the messages as a system message
            messages.append({"role": "system", "content": f"Order response: {order_response}"})
            print_with_voice(f"Order response: {order_response}")
        except Exception as e:
            # If there was an error creating the order, add that to the messages
            messages.append({"role": "system", "content": str(e)})
            print_with_voice(str(e))

    elif matched_endpoint == "continue_order":
        matched_endpoint = input("Enter 'ok' to continue creating orders or press Enter to exit: ")
    elif matched_endpoint == "backtest_strategy":
            # Ask the user for the strategy they want to backtest
            strategy_name = input("Enter the name of the strategy you want to backtest: ")
            
            # Here you need to provide the data for backtesting, assuming it is stored in a CSV file
            df = pd.read_csv(r'C:\Users\kingp\Downloads\Trading_Pal-main\Trading_Pal-main\GBP_USD_D.csv')

            # Create a Strategies instanc
            strategies = Strategies(df)

            # Call the corresponding method based on the strategy name
            if strategy_name.lower() == "rsi and macd crossover strategy":
                backtest_result = strategies.RSI_and_MACD_Crossover_Strategy()
            elif strategy_name.lower() == "Three MA Crossover Strategy":
                backtest_result = strategies.Three_MA_Crossover_Strategy()
            else:
                print_with_voice("Invalid strategy name!")
                

            # Assuming the backtest_result is a dictionary with keys 'total_return' and 'win_rate'
            # You need to modify this based on the actual structure of your backtest_result
            total_return = backtest_result['total_return']
            win_rate = backtest_result['win_rate']

            # Create a detailed message about the backtest
            detailed_message = f"The strategy '{strategy_name}' was backtested. The backtest showed a success rate of {total_return*100}%, with a total profit of ${win_rate}. This means that if you had used this strategy, you would have been successful {total_return*100}% of the time and made a total profit of ${win_rate}."

    else:
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": ""})
        response = create_chat_completion(messages)
        print_with_voice(response)
        messages[-1]["content"] = response
        messages.append({"role": "user", "content": ""})
    return jsonify({'response': response, 'error': error})

if __name__ == "__main__":
    app.run(debug=True)