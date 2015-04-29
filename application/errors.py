from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def init_errors(app):
    for code in [k for k, v in HTTP_STATUS_CODES.items() if k >= 400]:
        app.error_handler_spec[None][code] = error_handler


def error_handler(error):
    resp = jsonify(code=error.code,
                   name=error.name,
                   description=error.description)
    resp.status_code = error.code
    return resp
