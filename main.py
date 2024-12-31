import os
import logging
from dotenv import load_dotenv
from modules.order import Order
from modules.ticker import Ticker
from utils.indicators import calculate_sma, calculate_ema, calculate_macd

def load_api_keys():
    """API 키를 로드합니다."""
    access_key = os.getenv("UPBIT_ACCESS_KEY")
    secret_key = os.getenv("UPBIT_SECRET_KEY")
    if not access_key or not secret_key:
        raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
    return access_key, secret_key

def main():
    """프로그램 실행 함수"""

    # .env 파일에서 API 키 로드
    load_dotenv()
    try:
        access_key, secret_key = load_api_keys()
    except ValueError as ve:
        print(ve)
        return

    # Order 및 Ticker 객체 초기화
    order = Order(access_key=access_key, secret_key=secret_key)
    ticker = Ticker(fiat="KRW")  # 기본적으로 KRW 시장 티커 사용
    
    # Test code
    ohlcv_data = ticker.get_ohlcv("KRW-BTC", interval="day", count=5)


if __name__ == "__main__":
    main()
