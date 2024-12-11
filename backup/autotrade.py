import os
import time
import json
import pandas as pd
from dotenv import load_dotenv
import pyupbit
from openai import OpenAI

# Load environment variables
load_dotenv()

# Function to fetch all required data
def fetch_data():
    # Fetch account balance
    access = os.getenv("UPBIT_ACCESS_KEY")
    secret = os.getenv("UPBIT_SECRET_KEY")
    upbit = pyupbit.Upbit(access, secret)
    balance = upbit.get_balances()

    # Fetch order book data
    orderbook = pyupbit.get_orderbook(ticker="KRW-BTC")

    # Fetch OHLCV data (30-day daily candle)
    daily_ohlcv = pyupbit.get_ohlcv("KRW-BTC", count=30, interval="day")

    # Fetch OHLCV data (24-hour hourly candle)
    hourly_ohlcv = pyupbit.get_ohlcv("KRW-BTC", count=24, interval="minute60")

    return balance, orderbook, daily_ohlcv, hourly_ohlcv


def ai_trading():
    # 1. Fetch all necessary data
    balance, orderbook, daily_ohlcv, hourly_ohlcv = fetch_data()

    # Prepare data for AI
    data = {
        "balance": balance,
        "orderbook": orderbook,
        "daily_ohlcv": daily_ohlcv.to_dict(),
        "hourly_ohlcv": hourly_ohlcv.to_dict(),
    }

    # 2. Send data to AI for decision making
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in cryptocurrency trading. "
                    "Based on the provided data, make a decision whether to BUY, SELL, or HOLD Bitcoin. "
                    "Provide a JSON response with your decision and reason."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(data),
            },
        ]
    )

    # Parse AI response
    try:
        result = json.loads(response.choices[0].message.content)
        decision = result.get("decision", "hold").lower()
        reason = result.get("reason", "No reason provided")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing AI response: {e}")
        return

    # 3. Execute trade based on AI decision
    upbit = pyupbit.Upbit(
        os.getenv("UPBIT_ACCESS_KEY"), os.getenv("UPBIT_SECRET_KEY")
    )
    print(f"### AI Decision: {decision.upper()} ###")
    print(f"### Reason: {reason} ###")

    if decision == "buy":
        my_krw = upbit.get_balance("KRW")
        if my_krw * 0.9995 > 5000:
            print("### Executing Buy Order ###")
            # Uncomment the line below for actual trading
            # upbit.buy_market_order("KRW-BTC", my_krw * 0.9995)
        else:
            print("### Insufficient KRW to Buy ###")
    elif decision == "sell":
        my_btc = upbit.get_balance("BTC")
        current_price = pyupbit.get_current_price("KRW-BTC")
        if my_btc * current_price > 5000:
            print("### Executing Sell Order ###")
            # Uncomment the line below for actual trading
            # upbit.sell_market_order("KRW-BTC", my_btc)
        else:
            print("### Insufficient BTC to Sell ###")
    elif decision == "hold":
        print("### Holding Position ###")
    else:
        print("### Unknown Decision ###")


# Run the bot in a loop
if __name__ == "__main__":
    while True:
        ai_trading()
        time.sleep(10)
