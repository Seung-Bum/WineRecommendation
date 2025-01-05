from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['GET'])
def calculate():
    data = request.json
    try:
        num1 = float(data['num1'])
        num2 = float(data['num2'])
    except ValueError:
        return jsonify({'error': 'Invalid number format'}), 400

    num1 = float(data.get('num1'))
    num2 = float(data.get('num2'))
    operation = data.get('operation')

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
