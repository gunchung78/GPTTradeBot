import pyupbit
import pandas as pd
import numpy as np

def calculate_moving_averages(prices, short_window=20, long_window=50):
    # Create a DataFrame to store moving averages
    ma_df = pd.DataFrame(index=prices.index)
    ma_df['price'] = prices
    
    # Simple Moving Averages (SMA)
    ma_df[f'SMA_{short_window}'] = prices.rolling(window=short_window).mean()
    ma_df[f'SMA_{long_window}'] = prices.rolling(window=long_window).mean()
    
    # Exponential Moving Averages (EMA)
    ma_df[f'EMA_{short_window}'] = prices.ewm(span=short_window, adjust=False).mean()
    ma_df[f'EMA_{long_window}'] = prices.ewm(span=long_window, adjust=False).mean()

    return ma_df

def generate_signals(df):
    """
    Generate buy and sell signals based on Golden Cross and Death Cross.
    """
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0

    # Generate signals
    signals['signal'] = df['SMA_short'] > df['SMA_long']
    signals['signal'] = signals['signal'].astype(int)

    # Calculate buy and sell points
    signals['buy_signal'] = (signals['signal'] > signals['signal'].shift(1)).astype(int)
    signals['sell_signal'] = (signals['signal'] < signals['signal'].shift(1)).astype(int)

    return signals

def calculate_atr(df, period=14):
    # Calculate True Range (TR)
    df['previous_close'] = df['close'].shift(1)
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = abs(df['high'] - df['previous_close'])
    df['low_close'] = abs(df['low'] - df['previous_close'])
    df['true_range'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)

    # Calculate ATR
    atr = df['true_range'].rolling(window=period, min_periods=1).mean()

    return atr

def calculate_stop_loss_and_target(current_price, atr, atr_multiplier=2):
    stop_loss = current_price - (atr * atr_multiplier)
    target_price = current_price + (atr * atr_multiplier)
    return stop_loss, target_price

def calculate_rsi(df, period=14):
    delta = df['close'].diff()  # Calculate price changes

    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate average gains and losses
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    
    # Calculate RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def get_valid_tickers(fiat="KRW", interval="day", num=60):
    valid_tickers = []
    rsi = [] 
    tickers = pyupbit.get_tickers(fiat=fiat)  # Fetch all tickers for the given fiat
    
    for ticker in tickers:
        try:
            # Fetch OHLCV data
            df = pyupbit.get_ohlcv(ticker, interval=interval, count=num)
            if df is not None and len(df) >= num:  # Check if data length meets the requirement
                valid_tickers.append(ticker)
                df['RSI'] = calculate_rsi(df)
                today_rsi = df['RSI'].iloc[-1]
                rsi.append(int(today_rsi))
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    return valid_tickers, rsi

if __name__ == "__main__":
    valid_tickers, rsi = get_valid_tickers("KRW", "day", 60)
    for i in range(len(rsi)):
        print(valid_tickers[i],rsi[i])