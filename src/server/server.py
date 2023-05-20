from flask import Flask, jsonify, request

from src.predict import fill_mask_model

app = Flask(__name__)


@app.route('/api/fill_mask', methods=['POST'])
def fill_mask():
    data = request.get_json(force=True)
    output = fill_mask_model(data['x'])
    return jsonify({
        'input': data['x'],
        'output': output
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
