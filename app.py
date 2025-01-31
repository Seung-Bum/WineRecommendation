from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from recommend import recommend_wine, load_wine_data
from flask_cors import CORS


app = Flask(__name__, static_folder="static")
app.secret_key = "your_secret_key_here"  # 세션 사용을 위한 키 설정

# JSON 데이터 불러오기
wine_recommendations = load_wine_data()
print(" * Wine Data load complated:", len(wine_recommendations))


@app.route('/')
def index():
    return render_template('main.html')


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

    response = recommend_wine(data, wine_recommendations)
    print("response:", response)

    session['response'] = response  # 세션에 저장
    return jsonify({"redirect": "/result"})  # JSON 응답으로 리디렉트 URL 반환


@app.route('/result')
def result_page():
    response = session.pop('response', "No data available")  # 세션에서 데이터 가져오기
    return render_template('result.html', response=response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
CORS(app)
