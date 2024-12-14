import os
from dotenv import load_dotenv

class User:
    """API 키 관리를 위한 사용자 클래스"""

    def __init__(self, dotenv_path="../.env"):  # 상위 폴더 경로 지정
        """
        User 클래스 초기화
        :param dotenv_path: .env 파일 경로 (기본값: 상위 폴더)
        """
        self.dotenv_path = dotenv_path
        self.access_key = None
        self.secret_key = None
        self._load_api_keys()

    def _load_api_keys(self):
        """환경 변수에서 API 키를 로드"""
        try:
            load_dotenv(self.dotenv_path)  # 상위 폴더의 .env 파일 로드
            self.access_key = os.getenv("UPBIT_ACCESS_KEY")
            self.secret_key = os.getenv("UPBIT_SECRET_KEY")

            if not self.access_key or not self.secret_key:
                raise ValueError("API 키가 .env 파일에 설정되지 않았습니다.")
        except Exception as e:
            print(f"API 키 로드 실패: {e}")
            self.access_key = None
            self.secret_key = None

    def get_access_key(self):
        """Access Key 반환"""
        return self.access_key

    def get_secret_key(self):
        """Secret Key 반환"""
        return self.secret_key


# 테스트용 코드
if __name__ == "__main__":
    # 상위 폴더에 있는 .env 파일에서 API 키 로드
    user = User()

    # API 키 확인
    access_key = user.get_access_key()
    secret_key = user.get_secret_key()

    if access_key and secret_key:
        print(f"Access Key: {access_key}")
        print(f"Secret Key: {secret_key}")
    else:
        print("API 키가 제대로 설정되지 않았습니다.")
