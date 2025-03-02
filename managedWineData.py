import json
from managedJsonFile import get_Json_WineDesc, get_Json_WineData

# 와인 설명 딕셔너리 추가
wine_descriptions = get_Json_WineDesc()
wine_data = get_Json_WineData()


def recommend_wine(user_data, wine_recommendations):
    print("recommend_wine 시작")
    """
    사용자 데이터를 기반으로 추천 와인을 찾고, 와인 설명을 함께 반환하는 함수

    :param user_data: 사용자의 와인 선호 조건 (dict)
    :param wine_recommendations: 추천 와인 리스트 (list of dict)
    :return: {"wine": 추천 와인명, "description": 와인 설명} 또는 None
    """
    for recommendation in wine_recommendations:
        try:
            if all(user_data.get(key, None) == value for key, value in recommendation["conditions"].items()):
                wine_name = recommendation["wine"]
                return wine_name
        except Exception as e:
            print(f"Error while checking conditions: {e}")  # 오류 출력
    return None  # 조건에 맞는 와인이 없으면 None 반환


def get_wineData(wine):
    print("get_wineData: " + wine)
    wine_desc_json = get_Json_WineDesc()
    wine_info = wine_desc_json.get(wine)

    if not wine_info:  # 값이 None이거나 빈 딕셔너리일 때
        return {
            "wine": "",
            "description": "다시 선택 해주세요",
            "image_url": "/static/images/empty.jpg",
        }

    # 데이터가 정상적으로 존재하면 반환
    return {
        "wine": wine,
        "description": wine_info.get("description", "다시 선택 해주세요"),  # 기본값 제공
        # 기본 이미지 제공
        "image_url": wine_info.get("image_url", "/static/images/empty.jpg"),
    }


def load_wine_data():
    # print("load_wine_data 시작")

    try:
        # 각 데이터에 설명 추가
        for item in wine_data:
            wine_Name = item.get("wine")
            if wine_Name in wine_descriptions:
                item["description"] = wine_descriptions[wine_Name]  # 설명 추가
            else:
                item["description"] = "No description available for this wine."

        # print("load_wine_data 종료")
        return wine_data

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return []
