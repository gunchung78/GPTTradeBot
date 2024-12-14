import pyupbit
import logging
import csv
from datetime import datetime

class Order:
    """Upbit 주문 처리 클래스"""

    def __init__(self, access_key, secret_key):
        """
        Order 클래스 초기화
        :param access_key: 업비트 API Access Key
        :param secret_key: 업비트 API Secret Key
        """
        self.upbit = pyupbit.Upbit(access_key, secret_key)
        self.log_file = "error.log"
        self.history_file = "order_history.csv"
        self._setup_logging()
        self._setup_history_file()

    def _setup_logging(self):
        """에러 로깅 설정"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def _setup_history_file(self):
        """주문 이력 파일 초기화"""
        try:
            with open(self.history_file, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                # 헤더가 비어있을 경우에만 추가
                if csvfile.tell() == 0:
                    writer.writerow(["timestamp", "type", "ticker", "amount", "price", "result"])
        except Exception as e:
            logging.error(f"주문 이력 파일 초기화 실패: {e}")

    def log_error(self, message):
        """에러 메시지를 로그 파일에 기록"""
        logging.error(message)

    def save_order_history(self, order_type, ticker, amount, price, result):
        """
        주문 이력을 CSV 파일에 저장
        :param order_type: 주문 유형 ("buy" 또는 "sell")
        :param ticker: 티커 (예: "KRW-BTC")
        :param amount: 주문 수량 또는 금액
        :param price: 주문 가격
        :param result: 주문 결과
        """
        try:
            with open(self.history_file, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([datetime.now(), order_type, ticker, amount, price, result])
        except Exception as e:
            self.log_error(f"주문 이력 저장 실패: {e}")

    def get_balance(self, ticker="KRW"):
        """특정 티커의 잔고를 조회"""
        try:
            balance = self.upbit.get_balance(ticker)
            return float(balance)
        except Exception as e:
            self.log_error(f"잔고 조회 실패 (티커: {ticker}): {e}")
            return 0.0

    def buy_market_order(self, ticker, amount):
        """시장가 매수 주문 실행"""
        try:
            result = self.upbit.buy_market_order(ticker, amount)
            self.save_order_history("buy", ticker, amount, "market_price", result)
            return result
        except Exception as e:
            self.log_error(f"시장가 매수 실패 (티커: {ticker}, 금액: {amount}): {e}")
            return None

    def sell_market_order(self, ticker, quantity):
        """시장가 매도 주문 실행"""
        try:
            result = self.upbit.sell_market_order(ticker, quantity)
            self.save_order_history("sell", ticker, quantity, "market_price", result)
            return result
        except Exception as e:
            self.log_error(f"시장가 매도 실패 (티커: {ticker}, 수량: {quantity}): {e}")
            return None

    def get_order_status(self, ticker):
        """미체결 주문 상태 조회"""
        try:
            orders = self.upbit.get_order(ticker)
            return orders
        except Exception as e:
            self.log_error(f"미체결 주문 조회 실패 (티커: {ticker}): {e}")
            return []

    def cancel_order(self, uuid):
        """특정 주문 취소"""
        try:
            cancel_result = self.upbit.cancel_order(uuid)
            return cancel_result
        except Exception as e:
            self.log_error(f"주문 취소 실패 (UUID: {uuid}): {e}")
            return None


# 테스트용 코드
if __name__ == "__main__":
    # 여기에 자신의 Access Key와 Secret Key를 입력하세요
    ACCESS_KEY = "your-access-key"
    SECRET_KEY = "your-secret-key"

    # Order 클래스 초기화
    order = Order(ACCESS_KEY, SECRET_KEY)

    # 잔고 조회
    krw_balance = order.get_balance("KRW")
    print(f"보유 KRW 잔고: {krw_balance}")

    # 시장가 매수
    buy_result = order.buy_market_order("KRW-BTC", 5000)  # 5,000원으로 BTC 매수
    print("매수 결과:", buy_result)

    # 시장가 매도
    sell_result = order.sell_market_order("KRW-BTC", 0.0001)  # BTC 0.0001개 매도
    print("매도 결과:", sell_result)
