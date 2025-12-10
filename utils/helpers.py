# utils/helpers.py
from flask import jsonify
from dicttoxml import dicttoxml  # pip install dicttoxml

def format_response(data, response_format='json'):
    if response_format == 'xml':
        return dicttoxml(data), 200, {'Content-Type': 'application/xml'}
    return jsonify(data)
