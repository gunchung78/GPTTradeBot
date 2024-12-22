import pyupbit
import logging


class Order:
    """업비트 주문 처리 클래스"""

    def __init__(self, access_key, secret_key):
        """
        Order 클래스 초기화
        :param access_key: 업비트 API Access Key
        :param secret_key: 업비트 API Secret Key
        """
        if not access_key or not secret_key:
            raise ValueError("API 키가 제공되지 않았습니다.")

        self.upbit = pyupbit.Upbit(access_key, secret_key)

    def get_balance(self, ticker="KRW"):
        """
        특정 티커의 잔고를 조회합니다.
        :param ticker: 잔고를 조회할 티커 (예: "KRW", "KRW-BTC")
        :return: 잔고(float)
        """
        try:
            balance = self.upbit.get_balance(ticker)
            return float(balance)
        except Exception as e:
            logging.error(f"잔고 조회 실패 ({ticker}): {e}")
            return 0.0

    def buy_market_order(self, ticker, amount):
        """
        시장가 매수 주문을 실행합니다.
        :param ticker: 매수할 티커 (예: "KRW-BTC")
        :param amount: 매수 금액 (KRW)
        :return: 주문 결과 (dict) 또는 None
        """
        try:
            result = self.upbit.buy_market_order(ticker, amount)
            logging.info(f"시장가 매수 성공: {result}")
            return result
        except Exception as e:
            logging.error(f"시장가 매수 실패 ({ticker}, {amount}): {e}")
            return None

    def sell_market_order(self, ticker, quantity):
        """
        시장가 매도 주문을 실행합니다.
        :param ticker: 매도할 티커 (예: "KRW-BTC")
        :param quantity: 매도 수량
        :return: 주문 결과 (dict) 또는 None
        """
        try:
            result = self.upbit.sell_market_order(ticker, quantity)
            logging.info(f"시장가 매도 성공: {result}")
            return result
        except Exception as e:
            logging.error(f"시장가 매도 실패 ({ticker}, {quantity}): {e}")
            return None
