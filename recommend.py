import json
import os


def load_wine_data():
    # recommend.py와 같은 폴더에 위치한 경우
    # Windows에서는 static\data\wine.txt, Linux에서는 static/data/wine.txt로 자동 변환
    file_path = os.path.join("static", "data", "wine.txt")

    if not os.path.exists(file_path):  # 파일이 존재하는지 확인
        print(f"[ERROR] file path not existence: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()  # 공백 제거

            if not content:  # 파일이 비어 있을 경우 예외 처리
                raise ValueError("JSON is Empty!")

            return json.loads(content)  # JSON 문자열을 Python 객체로 변환
    except json.JSONDecodeError as e:
        print(f"JSON passing error: {e}")
        return []
    except FileNotFoundError:
        print("file not founded")
        return []


def recommend_wine(user_data, wine_recommendations):  # 와인 추천 로직 구현

    # 추천 와인 찾기
    for recommendation in wine_recommendations:
        try:
            if all(user_data.get(key, None) == value for key, value in recommendation["conditions"].items()):
                return recommendation["wine"]
        except Exception as e:
            print(f"Error while checking conditions: {e}")  # 오류 출력

    # 기본 추천
    return "No exact match found"


# 테스트
# 사용자가 선택한 데이터 예시
# user_data = {
#     "smell": "fruitsmell",
#     "fruit": "strawberry",
#     "food": "steak",
#     "proof": "strong",
#     "feel": "diversion",
#     "texture": "thick",
#     "budget": "daily"
# }

# 와인 추천 실행
# result = recommend_wine(user_data)
# print("result:", result)
