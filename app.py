# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify, session, Response
from managedWineData import recommend_wine, get_wineData, load_wine_data, recommend_wine_by_tags
from managedJsonFile import get_Json_WineDesc
from decryptKey import decrypt_secret_key
from flask_cors import CORS
from config import config, server_config, get_lang_config
from flask import send_from_directory
import os
import json

app = Flask(__name__, static_folder="static")
CORS(app)  # 다른 도메인에서 오는 요청을 Flask 서버가 허용할 수 있도록 설정하는 역할
encrypted_secret_key, decryption_key, env, port = server_config()

# 복호화한 SECRET_KEY 적용
app.secret_key = decrypt_secret_key(encrypted_secret_key, decryption_key)
# print(f" * Decrypted SECRET_KEY: {app.secret_key}")

app.config.from_object(config[env])
print(f" * FLASK_ENV: {env}")

# WINE JSON 데이터 불러오기
wine_recommendations = load_wine_data()
print(" * Wine Data load complated:", len(wine_recommendations))


@app.route('/<filename>.html')  # 루트 경로에서 HTML 파일 제공
def serve_static_html(filename):
    return send_from_directory(os.getcwd(), f"{filename}.html")


@app.route('/robots.txt')  # robots.txt 서빙
def robots():
    return send_from_directory(os.getcwd(), 'robots.txt')


@app.route('/sitemap.xml')  # sitemap.xml 서빙
def sitemap():
    return send_from_directory(os.getcwd(), 'sitemap.xml')


@app.route("/config")  # 클라이언트에서 요청시에 현재 환경 리턴
def get_config():
    return jsonify({"api_base_url": app.config["API_BASE_URL"]})


@app.route('/')  # 메인페이지 이동
def main_page():
    return render_template("main.html")


@app.route('/finder')  # 태그 찾기
def finder_page():
    return render_template("finder.html")


@app.route('/character')
def character_page():
    # 언어별 web 페이지 경로 설정
    lang_code = get_lang_config()
    return render_template(f"main_web_{lang_code}.html")


@app.route('/getWineData', methods=['GET'])
def get_wine_data():
    tags_param = request.args.get('tags')

    if tags_param:
        selected_tags = tags_param.split(",")
        # 선택된 태그가 모두 포함된 와인만 필터링
        filtered_wines = recommend_wine_by_tags(
            selected_tags, wine_recommendations)

        # for wine in filtered_wines:
        #    print(f"추천 와인: {wine}")
    else:
        data = get_Json_WineDesc()  # UTF-8로 읽었음 (태그 선택 없을시 전체 반환)
        json_str = json.dumps(data, ensure_ascii=False)  # 한글 깨짐 방지
        return Response(json_str, content_type='application/json; charset=utf-8')

    # 리스트를 딕셔너리로 변환 (프론트에서 Object.values(data) 사용 중이라서)
    response_data = {str(i): wine for i, wine in enumerate(filtered_wines)}
    return jsonify(response_data)


@app.route('/receiveData', methods=['POST'])  # 사용자 데이터를 받아서 취향 확인
def recommand():
    # Content-Type 확인
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400

    # 사용자 JSON 데이터 파싱
    userData = request.get_json(silent=True)
    if not userData:
        return jsonify({"error": "Invalid JSON data"}), 400

    # 받은 데이터 출력
    print(f"Received Keyword: {userData}")

    # 와인 종류에 따라 다른 데이터 나가게
    wineName = recommend_wine(userData, wine_recommendations)
    print("recommand:", wineName)

    # return redirect(url_for('result_page', wineName=wineName))  # 직접 리다이렉트
    # 🛠 wineName을 포함한 URL로 리디렉트 정보 반환 (이전에는 JSON 응답만 했음)
    return jsonify({"redirect": f"/result?wineName={wineName}"})


@app.route('/result')
def result_page():
    # 🛠 URL에서 wine 값을 가져옴 (세션 대신)
    wineName = request.args.get('wineName', "No data available")
    print("result_page: " + wineName)
    wineData = get_wineData(wineName)
    print("get_wineData: " + wineName)

    session['response'] = wineData  # 세션에 저장
    userSession = session.get('response', "No data available")  # 세션에서 데이터 가져오기

    lang_code = get_lang_config()
    return render_template(f"result_web_{lang_code}.html", wineData=wineData, userSession=userSession)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=(env == "development"))
