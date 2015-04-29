from __future__ import absolute_import

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import Forbidden


class Login(MethodView):

    def post(self):
        data = request.get_json()
        user = data.get('username')
        if not user:
            raise Forbidden()
        return jsonify(token=user)


login = Login.as_view('login')
