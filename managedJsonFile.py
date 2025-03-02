import os
import json
from config import get_lang_config


def get_Json_WineDesc():
    """결과 페이지 호출시 매번 실행"""
    # 언어별 JSON 파일 경로 설정
    lang_code = get_lang_config()
    file_name = f"wine_descriptions_{lang_code}.json"
    file_path = os.path.join("static", "data", file_name)
    # print(" * lang_code : " + lang_code)

    # file_path = os.path.join("static", "data", "wine_descriptions.json")
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            wine_desc_json = json.load(f)  # JSON을 Python 딕셔너리로 로드
        except json.JSONDecodeError:
            raise ValueError("JSON 파일을 제대로 읽을 수 없습니다!")

    if not wine_desc_json:
        raise ValueError("JSON 파일이 비어 있습니다!")
    # print("✅ getWineDesc, JSON 데이터 로드 완료:", len(wine_desc_json))

    return wine_desc_json


def get_Json_WineData():
    file_path = os.path.join("static", "data", "wine.json")
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            content = json.load(f)  # JSON을 Python 딕셔너리로 로드
        except json.JSONDecodeError:
            raise ValueError("JSON 파일을 제대로 읽을 수 없습니다!")

    if not content:
        raise ValueError("JSON 파일이 비어 있습니다!")
    # print("✅ getWineData, JSON 데이터 로드 완료:", len(content))

    return content
