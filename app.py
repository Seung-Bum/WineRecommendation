import os
from flask import Flask, request, render_template, jsonify, session
from recommend import recommend_wine, load_wine_data
from decryptKey import decrypt_secret_key
from dotenv import load_dotenv
from flask_cors import CORS
from config import config


app = Flask(__name__, static_folder="static")

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
encrypted_secret_key = os.getenv("ENCRYPTED_SECRET_KEY")
decryption_key = os.getenv("DECRYPTION_KEY")

# 복호화한 SECRET_KEY 적용
app.secret_key = decrypt_secret_key(encrypted_secret_key, decryption_key)
# print(f" * Decrypted SECRET_KEY: {app.secret_key}")

# 환경 변수에 따라 설정 적용
# 기본값은 'production' (이 문장에서 FLASK_ENV가 환경변수를 가져오는 소스임)
# .env의 FLASK_ENV에 따라 값 달라짐
env = os.getenv("FLASK_ENV", "production")
app.config.from_object(config[env])
print(f" * FLASK_ENV: {env}")

# 환경 변수에서 PORT 값 가져오기 (없으면 기본값 8080)
port = int(os.environ.get("PORT", 8080))

# WINE JSON 데이터 불러오기
wine_recommendations = load_wine_data()
print(" * Wine Data load complated:", len(wine_recommendations))


@app.route("/config")
def get_config():
    return jsonify({"api_base_url": app.config["API_BASE_URL"]})


@app.route('/')
def index():
    return render_template("main_web.html")


@app.route('/recommend', methods=['POST'])
def recommend():

    # Content-Type 확인
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400

    # JSON 데이터 파싱
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # 받은 데이터 출력
    print(f"Received Keyword: {data}")

    # 와인 종류에 따라 다른 데이터 나가게
    response = recommend_wine(data, wine_recommendations)
    print("response:", response)

    if response == None:
        response = {'wine': '', 'description': '다시 선택 해주세요',
                    'image_url': '/static/images/empty.jpg'}

    session['response'] = response  # 세션에 저장
    return jsonify({"redirect": "/result"})  # JSON 응답으로 리디렉트 URL 반환


@app.route('/result')
def result_page():
    response = session.pop('response', "No data available")  # 세션에서 데이터 가져오기
    return render_template("result_web.html", response=response)


# def web_division():
#     user_agent = request.headers.get('User-Agent', '').lower()
#     if "mobile" in user_agent or "android" in user_agent or "iphone" in user_agent:
#         return "mobile"
#     else:
#         return "web"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=(env == "development"))
CORS(app)  # 다른 도메인에서 오는 요청을 Flask 서버가 허용할 수 있도록 설정하는 역할
