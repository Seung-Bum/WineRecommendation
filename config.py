import os
from dotenv import load_dotenv
from flask import request, has_request_context


class Config:
    API_BASE_URL = os.getenv(
        "API_BASE_URL", "http://localhost:5000")  # 기본값은 로컬


class ProductionConfig(Config):
    API_BASE_URL = "http://124.51.107.175:5001"


class DevelopmentConfig(Config):
    API_BASE_URL = "http://localhost:5000"


# 딕셔너리
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}


def get_lang_config():
    """사용자의 'Accept-Language' 헤더를 기반으로 언어 설정을 반환(기본값 en)"""
    if has_request_context():  # 현재 요청 컨텍스트가 있는지 확인
        user_lang = request.headers.get("Accept-Language", "en")
        return "ko" if "ko" in user_lang else "en"
    return "en"  # 컨텍스트가 없으면 기본값 반환


def server_config():
    # .env 파일 로드
    load_dotenv()

    # 환경 변수 가져오기 (config.py)
    encrypted_secret_key = os.getenv("ENCRYPTED_SECRET_KEY")
    decryption_key = os.getenv("DECRYPTION_KEY")

    # 환경 변수에서 PORT 값 가져오기 (없으면 기본값 5001, 개발은 5000)
    port = int(os.environ.get("PORT", 5001))

    # 환경 변수에 따라 설정 적용 (.env의 FLASK_ENV에 따라 값 달라짐)
    # 기본값은 'production' (이 문장에서 FLASK_ENV가 환경변수를 가져오는 키)
    env = os.getenv("FLASK_ENV", "production")

    return encrypted_secret_key, decryption_key, env, port
