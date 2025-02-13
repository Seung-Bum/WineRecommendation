import os


class Config:
    API_BASE_URL = os.getenv(
        "API_BASE_URL", "http://localhost:5000")  # 기본값은 로컬


class ProductionConfig(Config):
    API_BASE_URL = "http://124.51.107.175:8080"


class DevelopmentConfig(Config):
    API_BASE_URL = "http://localhost:5000"


# 딕셔너리
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
