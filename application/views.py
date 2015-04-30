from flask import jsonify, request
from flask.views import MethodView
from functools import wraps
from jwt.exceptions import DecodeError
from werkzeug.exceptions import Forbidden, NotFound

from application.models import Item, User


def authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if User.by_token(request.headers.get('X-Auth-Token', '')):
                return f(*args, **kwargs)
        except DecodeError:
            pass
        raise Forbidden()
    return decorated_function


class ItemView(MethodView):

    decorators = [authenticated]

    def get(self, id=None):
        if not id:
            items = Item.query.filter(Item.is_bought == 0).all()
            return jsonify(items=[item.as_dict() for item in items])
        item = Item.query.get(id)
        if not item:
            raise NotFound()
        return jsonify(item.as_dict())


class LoginView(MethodView):

    def post(self):
        data = request.get_json()
        user = User.by_username(data.get('username', ''))
        if not user or not user.check_password(data.get('password', '')):
            raise Forbidden()
        return jsonify(token=user.token())


item = ItemView.as_view('item')
login = LoginView.as_view('login')
