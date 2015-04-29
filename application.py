#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def ip():
    return request.environ['REMOTE_ADDR'] + '\n'


if __name__ == '__main__':
    app.run()
