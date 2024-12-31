import pandas as pd

def calculate_sma(prices, period):
    """
    단순이동평균(SMA) 계산
    """
    if not isinstance(prices, (list, pd.Series)):
        raise ValueError("가격 데이터는 리스트 또는 Pandas Series여야 합니다.")
    return pd.Series(prices).rolling(window=period).mean()


def calculate_ema(prices, period):
    """
    지수이동평균(EMA) 계산
    """
    if not isinstance(prices, (list, pd.Series)):
        raise ValueError("가격 데이터는 리스트 또는 Pandas Series여야 합니다.")
    return pd.Series(prices).ewm(span=period, adjust=False).mean()


def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    """
    MACD 계산
    """
    if not isinstance(prices, (list, pd.Series)):
        raise ValueError("가격 데이터는 리스트 또는 Pandas Series여야 합니다.")
    prices = pd.Series(prices)
    ema_short = prices.ewm(span=short_period, adjust=False).mean()
    ema_long = prices.ewm(span=long_period, adjust=False).mean()
    macd_line = ema_short - ema_long
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_histogram = macd_line - signal_line
    return pd.DataFrame({
        "MACD_Line": macd_line,
        "Signal_Line": signal_line,
        "MACD_Histogram": macd_histogram
    })


def calculate_rsi(prices, period=14):
    """
    RSI (Relative Strength Index) 계산
    """
    if not isinstance(prices, (list, pd.Series)):
        raise ValueError("가격 데이터는 리스트 또는 Pandas Series여야 합니다.")
    prices = pd.Series(prices)
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(span=period, adjust=False).mean()
    avg_loss = loss.ewm(span=period, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
