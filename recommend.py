import json
import os

# 와인 설명 딕셔너리 추가
wine_descriptions = {
    "Riesling": {
        "description": "Riesling is a crisp and aromatic white wine with notes of citrus and stone fruit. \nIt pairs well with seafood and spicy dishes.",
        "image_url": "/static/images/riesling.jpg"
    },
    "Merlot": {
        "description": "Merlot is a smooth and medium-bodied red wine with flavors of plum, black cherry, and vanilla.",
        "image_url": "/static/images/merlot.jpg"
    },
    "Cabernet Sauvignon": {
        "description": "Cabernet Sauvignon is a bold and full-bodied red wine known for its dark fruit flavors and firm tannins.",
        "image_url": "/static/images/cabernet_sauvignon.jpg"
    },
    "Chardonnay": {
        "description": "Chardonnay is a popular white wine with rich, \nbuttery flavors and hints of oak and tropical fruit.",
        "image_url": "/static/images/chardonnay.jpg"
    },
    "Pinot Noir": {
        "description": "Pinot Noir is a light to medium-bodied red wine with elegant flavors of red berries and earthy notes.",
        "image_url": "/static/images/pinot_noir.jpg"
    },
    "Sauvignon Blanc": {
        "description": "A popular and unmistakable white wine that’s loved for its “green” herbal flavors and racy acidity. \nSauvignon Blanc grows nearly everywhere and, thus, offers a variety of styles ranging from lean to bountiful.",
        "image_url": "/static/images/sauvignon_blanc.jpg"
    },
    "Zinfandel": {
        "description": "Zinfandel wine is a bold, fruit-forward red loved for its jammy fruit and smoky, exotic spice notes. \nIt’s also made into a sweet rosé called White Zinfandel.",
        "image_url": "/static/images/zinfandel.jpg"
    }
}


def load_wine_data():
    file_path = os.path.join("static", "data", "wine.txt")

    if not os.path.exists(file_path):
        print(f"[ERROR] file path not existence: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                raise ValueError("JSON is Empty!")

            wine_data = json.loads(content)

            # 각 데이터에 설명 추가
            for item in wine_data:
                wine_type = item.get("wine")
                if wine_type in wine_descriptions:
                    item["description"] = wine_descriptions[wine_type]  # 설명 추가
                else:
                    # 기본 설명
                    item["description"] = "No description available for this wine."

            return wine_data

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return []
    except FileNotFoundError:
        print("File not found")
        return []


def recommend_wine(user_data, wine_recommendations):
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
                wine_data = wine_descriptions.get(
                    wine_name, "No description available.")  # 설명 추가

                # 와인 + 설명 반환
                return {"wine": wine_name, "description": wine_data["description"], "image_url": wine_data["image_url"]}
        except Exception as e:
            print(f"Error while checking conditions: {e}")  # 오류 출력

    return None  # 조건에 맞는 와인이 없으면 None 반환
