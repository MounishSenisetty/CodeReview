from flask import Flask, request, jsonify
from main import analyze_code

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_code1():
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'error': 'Missing code parameter'}), 400
    
    print(data["code"])
    report = analyze_code(input_code = data['code'])
    return jsonify({'report': report})

if __name__ == '__main__':
    app.run(debug=True)
