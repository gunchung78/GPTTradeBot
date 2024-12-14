from modules.ticker import Ticker

def display_menu():
    """사용자 메뉴를 출력합니다."""
    print("\n=== 가상화폐 자동매매 프로그램 ===")
    print("1. 특정 시장 티커 조회")
    print("2. 특정 티커 현재가 조회")
    print("3. 모든 티커 현재가 조회")
    print("4. 프로그램 종료")
    print("===============================")

def main():
    """메인 실행 함수"""
    # 기본적으로 KRW 시장의 티커를 초기화
    ticker = Ticker(fiat="KRW")
    
    while True:
        display_menu()
        choice = input("원하는 작업을 선택하세요: ")

        if choice == "1":
            print("\n[1] 특정 시장 티커 조회")
            market = input("시장 통화를 입력하세요 (예: KRW, BTC, USDT): ").upper()
            ticker = Ticker(fiat=market)
            ticker.display_tickers()
        
        elif choice == "2":
            print("\n[2] 특정 티커 현재가 조회")
            ticker_name = input("티커를 입력하세요 (예: KRW-BTC): ").upper()
            try:
                price = ticker.get_current_price(ticker_name)
                print(f"현재 {ticker_name} 가격: {price}")
            except Exception as e:
                print("에러 발생:", e)

        elif choice == "3":
            print("\n[3] 모든 티커 현재가 조회")
            try:
                prices = ticker.get_all_prices()
                print("모든 티커의 현재가:")
                for ticker_name, price in prices.items():
                    print(f"{ticker_name}: {price}")
            except Exception as e:
                print("에러 발생:", e)

        elif choice == "4":
            print("\n프로그램을 종료합니다.")
            break
        
        else:
            print("\n잘못된 선택입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()
