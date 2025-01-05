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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
