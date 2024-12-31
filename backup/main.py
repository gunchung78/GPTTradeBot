from dotenv import load_dotenv
from modules.order import Order
from modules.ticker import Ticker
from utils.indicators import calculate_sma, calculate_ema, calculate_macd

import os
import logging

# 로깅 설정
logging.basicConfig(filename="error.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


def load_api_keys():
    """API 키를 로드합니다."""
    access_key = os.getenv("UPBIT_ACCESS_KEY")
    secret_key = os.getenv("UPBIT_SECRET_KEY")
    if not access_key or not secret_key:
        raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
    return access_key, secret_key


def display_menu():
    """사용자 메뉴를 출력합니다."""
    print("\n=== 가상화폐 자동매매 프로그램 ===")
    print("1. 잔고 조회")
    print("2. 시장가 매수")
    print("3. 시장가 매도")
    print("4. 티커 목록 조회")
    print("5. 이동평균 계산 (SMA/EMA)")
    print("6. MACD 계산")
    print("7. 프로그램 종료")
    print("===============================")


def calculate_moving_averages(ticker):
    """SMA 및 EMA 계산을 수행합니다."""
    try:
        interval = input("캔들 간격을 입력하세요 (예: day, minute1) [기본값: day]: ") or "day"
        count = int(input("데이터 개수를 입력하세요 (기본값: 10): ") or 10)
        sma_period = int(input("SMA 기간을 입력하세요 (기본값: 3): ") or 3)
        ema_period = int(input("EMA 기간을 입력하세요 (기본값: 3): ") or 3)

        ticker_name = input("이동평균을 계산할 티커를 입력하세요 (예: KRW-BTC): ").upper()
        ohlcv_data = ticker.get_ohlcv(ticker_name, interval=interval, count=count)

        if ohlcv_data.empty:
            print(f"{ticker_name}에 대한 데이터를 가져올 수 없습니다.")
            return

        close_prices = ohlcv_data['close']
        sma = calculate_sma(close_prices, sma_period)
        ema = calculate_ema(close_prices, ema_period)

        print(f"\n=== {ticker_name} 이동평균 계산 결과 ===")
        print(f"SMA({sma_period}):")
        print(sma)
        print(f"\nEMA({ema_period}):")
        print(ema)
    except Exception as e:
        print("이동평균 계산 중 오류가 발생했습니다.")
        logging.error(f"이동평균 계산 실패: {e}")


def calculate_macd_analysis(ticker):
    """MACD 계산을 수행합니다."""
    try:
        interval = input("캔들 간격을 입력하세요 (예: day, minute1) [기본값: day]: ") or "day"
        count = int(input("데이터 개수를 입력하세요 (기본값: 26): ") or 26)
        ticker_name = input("MACD를 계산할 티커를 입력하세요 (예: KRW-BTC): ").upper()

        ohlcv_data = ticker.get_ohlcv(ticker_name, interval=interval, count=count)

        if ohlcv_data.empty:
            print(f"{ticker_name}에 대한 데이터를 가져올 수 없습니다.")
            return

        close_prices = ohlcv_data['close']
        macd_result = calculate_macd(close_prices)

        print(f"\n=== {ticker_name} MACD 계산 결과 ===")
        print(macd_result)
    except Exception as e:
        print("MACD 계산 중 오류가 발생했습니다.")
        logging.error(f"MACD 계산 실패: {e}")


def handle_choice(choice, order, ticker):
    """사용자의 선택에 따라 작업을 처리합니다."""
    try:
        if choice == "1":
            print("\n[1] 잔고 조회")
            ticker_name = input("잔고를 확인할 티커를 입력하세요 (예: KRW, KRW-BTC): ").upper()
            balance = order.get_balance(ticker_name)
            print(f"{ticker_name} 잔고: {balance}")

        elif choice == "2":
            print("\n[2] 시장가 매수")
            ticker_name = input("매수할 티커를 입력하세요 (예: KRW-BTC): ").upper()
            amount = float(input("매수 금액(KRW)을 입력하세요: "))
            result = order.buy_market_order(ticker_name, amount)
            print("매수 결과:", result)

        elif choice == "3":
            print("\n[3] 시장가 매도")
            ticker_name = input("매도할 티커를 입력하세요 (예: KRW-BTC): ").upper()
            quantity = float(input("매도 수량을 입력하세요: "))
            result = order.sell_market_order(ticker_name, quantity)
            print("매도 결과:", result)

        elif choice == "4":
            print("\n[4] 티커 목록 조회")
            ticker.display_tickers()

        elif choice == "5":
            print("\n[5] 이동평균 계산 (SMA/EMA)")
            calculate_moving_averages(ticker)

        elif choice == "6":
            print("\n[6] MACD 계산")
            calculate_macd_analysis(ticker)

        elif choice == "7":
            print("\n프로그램을 종료합니다.")
            return False

        else:
            print("\n잘못된 선택입니다. 다시 시도하세요.")
    except Exception as e:
        print("작업 중 오류가 발생했습니다. 로그를 확인하세요.")
        logging.error(f"작업 처리 실패: {e}")
    return True


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

    while True:
        display_menu()
        choice = input("원하는 작업을 선택하세요: ")
        if not handle_choice(choice, order, ticker):
            break


if __name__ == "__main__":
    main()
