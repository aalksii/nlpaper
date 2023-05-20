from flask import Flask, jsonify, request

from predict import fill_mask, summarize

app = Flask(__name__)


@app.route('/api/fill_mask', methods=['POST'])
def fill_mask_():
    data = request.get_json(force=True)
    output = fill_mask(data['x'])
    return jsonify({
        'input': data['x'],
        'output': output
    })


@app.route('/api/summarize', methods=['POST'])
def summarize_():
    data = request.get_json(force=True)
    output = summarize(data['x'])
    return jsonify({
        'input': data['x'],
        'output': output
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
