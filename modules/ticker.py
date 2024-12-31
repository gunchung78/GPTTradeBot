import pyupbit
import pandas as pd

class Ticker:
    """업비트 암호화폐 티커와 관련된 기능 제공"""

    def __init__(self, fiat="KRW"):
        """
        Ticker 클래스 초기화
        :param fiat: 조회할 시장의 통화 (기본값: "KRW")
        """
        self.fiat = fiat
        self.tickers = pyupbit.get_tickers(fiat=fiat)

    @staticmethod
    def get_current_price(tickers):
        """
        입력받은 티커(들)의 현재가를 조회합니다.
        :param tickers: 티커 문자열 또는 리스트 (ex: "KRW-BTC" 또는 ["KRW-BTC", "KRW-ETH"])
        :return: 현재가 (float 또는 dict)
        """
        return pyupbit.get_current_price(tickers)

    @staticmethod
    def get_ohlcv(ticker, interval="day", count=200):
        """
        특정 티커의 OHLCV 데이터를 조회합니다.
        :param ticker: 조회할 티커 (ex: "KRW-BTC")
        :param interval: 캔들 간격 (default: "day")
                         minute1, minute3, minute5, minute10, minute15,
                         minute30, minute60, minute240, day, week, month
        :param count: 조회할 데이터 개수 (default: 200)
        :return: OHLCV 데이터 (pandas.DataFrame)
        """
        try:
            df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
            if df is not None:
                return df.to_json()
            else:
                pass
                return pd.DataFrame()
        except Exception as e:
            print(f"OHLCV 데이터 조회 실패 ({ticker}): {e}")
            return pd.DataFrame()

    def display_tickers(self):
        """
        현재 설정된 시장의 티커 목록을 출력합니다.
        """
        print(f"{self.fiat} 시장의 티커 목록:")
        for ticker in self.tickers:
            print(ticker)

    def get_all_prices(self):
        """
        현재 선택된 시장의 모든 티커에 대한 현재가를 조회합니다.
        :return: 티커와 현재가의 딕셔너리 (dict)
        """
        return self.get_current_price(self.tickers)

if __name__ == "__main__":
    ticker = Ticker(fiat="KRW")

    # # 1. 티커 목록 출력
    # ticker.display_tickers()

    # # 2. 특정 티커의 현재가 조회
    # btc_price = ticker.get_current_price("KRW-BTC")
    # print(f"현재 KRW-BTC 가격: {btc_price}")

    # # 3. 모든 티커의 현재가 조회
    # all_prices = ticker.get_all_prices()
    # print("KRW 시장 모든 티커의 현재가:", all_prices)

    # 4. 특정 티커의 OHLCV 데이터 조회
    ohlcv_data = ticker.get_ohlcv("KRW-BTC", interval="day", count=5)
    print("KRW-BTC OHLCV 데이터:")
    print(ohlcv_data)

