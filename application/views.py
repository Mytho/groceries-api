from flask import jsonify, request
from flask.views import MethodView
from functools import wraps
from werkzeug.exceptions import Forbidden, NotFound

from application.models import User


def authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if User.by_token(request.headers.get('X-Auth-Token', '')):
                return f(*args, **kwargs)
        except:
            pass
        raise Forbidden()
    return decorated_function


class Item(MethodView):

    decorators = [authenticated]

    def get(self, id=None):
        if not id:
            return jsonify([item.as_dict() for item in Item.query.all()])
        item = Item.query.filter(Item.id == id).first()
        if not item:
            raise NotFound()
        return jsonify(item.as_dict())


class Login(MethodView):

    def post(self):
        data = request.get_json()
        user = User.by_username(data.get('username', ''))
        if not user or not user.check_password(data.get('password', '')):
            raise Forbidden()
        return jsonify(token=user.token())


item = Item.as_view('item')
login = Login.as_view('login')
