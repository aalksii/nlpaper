import click
from flask import Flask, jsonify, request

from configs.server_config import rest_api_port
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


@click.command
@click.option('--port',
              default=rest_api_port,
              help='Port for REST API')
def run(port):
    app.run(debug=True, port=port)


if __name__ == '__main__':
    run()
