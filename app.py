from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['GET'])
def calculate():
    print('headers: ' + str(request.headers))
    print('data: ' + str(request.args))

    try:
        num1 = float(request.args.get('num1'))
        num2 = float(request.args.get('num2'))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid number format'}), 400

    operation = request.args.get('operation')

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 == 0:
            return jsonify({'error': 'Cannot divide by zero'}), 400
        result = num1 / num2
    else:
        return jsonify({'error': 'Invalid operation'}), 400

    return jsonify({'result': result})


@app.route('/analyze', methods=['POST'])
def analyze():
    # Content-Type 확인
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400

    # JSON 데이터 파싱
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    # 받은 데이터 출력
    print(f"Received data: {data}")
    return jsonify({"message": "POST request received", "received": data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
