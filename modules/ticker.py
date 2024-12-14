import pyupbit

class Ticker:
    """업비트 암호화폐 티커와 관련된 기능 제공"""

    def __init__(self, fiat="KRW"):
        """
        Ticker 클래스 초기화
        :param fiat: 조회할 시장의 통화 (기본값: "KRW")
        """
        self.fiat = fiat
        self.tickers = self._get_tickers_by_fiat(fiat)

    @staticmethod
    def _get_all_tickers():
        """
        업비트에서 지원하는 모든 티커를 가져옵니다.
        :return: 티커 목록 (list)
        """
        return pyupbit.get_tickers()

    @staticmethod
    def get_current_price(tickers):
        """
        입력받은 티커(들)의 현재가를 조회합니다.
        :param tickers: 티커 문자열 또는 리스트 (ex: "KRW-BTC" 또는 ["KRW-BTC", "KRW-ETH"])
        :return: 현재가 (float 또는 dict)
        """
        return pyupbit.get_current_price(tickers)

    def _get_tickers_by_fiat(self, fiat):
        """
        특정 시장(fiat)의 티커 목록을 가져옵니다.
        :param fiat: 조회할 시장의 통화 (ex: "KRW", "BTC", "USDT")
        :return: 해당 시장의 티커 목록 (list)
        """
        return pyupbit.get_tickers(fiat=fiat)

    def get_all_prices(self):
        """
        현재 선택된 시장의 모든 티커에 대한 현재가를 조회합니다.
        :return: 티커와 현재가의 딕셔너리 (dict)
        """
        return self.get_current_price(self.tickers)

    def display_tickers(self):
        """
        현재 설정된 시장의 티커 목록을 출력합니다.
        """
        print(f"{self.fiat} 시장의 티커 목록:")
        for ticker in self.tickers:
            print(ticker)


# 테스트용 코드
if __name__ == "__main__":
    ticker = Ticker(fiat="KRW")  # KRW 시장 티커만 조회
    ticker.display_tickers()    # 티커 목록 출력
    
    # 특정 티커의 현재가 조회
    btc_price = ticker.get_current_price("KRW-BTC")
    print(f"현재 KRW-BTC 가격: {btc_price}")

    # 여러 티커의 현재가 조회
    prices = ticker.get_current_price(["KRW-BTC", "KRW-ETH"])
    print("현재가 정보:", prices)

    # KRW 시장 모든 티커의 현재가 조회
    all_prices = ticker.get_all_prices()
    print("KRW 시장 모든 티커의 현재가:", all_prices)
