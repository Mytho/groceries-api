from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import Forbidden

from application.models import User


class Login(MethodView):

    def post(self):
        data = request.get_json()
        user = User.by_username(data.get('username'))
        if not user:
            raise Forbidden()
        return jsonify(token=user.token())


login = Login.as_view('login')
