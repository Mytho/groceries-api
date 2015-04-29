#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/')
def ip():
    origin = request.headers.get('X-Forwarded-For', request.remote_addr)
    return jsonify(origin=origin)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
