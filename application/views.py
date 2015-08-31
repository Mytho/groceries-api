import sqlalchemy as sa
from flask import jsonify, request
from flask.views import MethodView
from functools import wraps
from jwt.exceptions import DecodeError
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from application.models import Item, User, db


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
            items = Item.query.filter(Item.is_bought == bool(0))\
                        .order_by(Item.created)\
                        .all()
            return jsonify(items=[item.as_dict() for item in items])
        item = Item.query.get(id)
        if not item:
            raise NotFound()
        return jsonify(item.as_dict())

    def post(self):
        data = request.get_json()
        item = Item(name=data.get('name'))
        db.session.add(item)
        db.session.commit()
        return jsonify(item.as_dict())

    def put(self, id=None):
        if not id:
            raise BadRequest()
        item = Item.query.get(id)
        if not item:
            raise NotFound()
        item.is_bought = not item.is_bought
        db.session.commit()
        return jsonify(item.as_dict())

    def delete(self, id=None):
        if not id:
            raise BadRequest()
        item = Item.query.get(id)
        if not item:
            raise NotFound()
        db.session.delete(item)
        db.session.commit()
        return jsonify(status='ok')


class LoginView(MethodView):

    def post(self):
        data = request.get_json()
        user = User.by_username(data.get('username', ''))
        if not user or not user.check_password(data.get('password', '')):
            raise Forbidden()
        return jsonify(token=user.token().decode('utf-8'))


class StatusView(MethodView):

    def get(self):
        try:
            db.session.query(sa.func.count(Item.id).label('count')).all()
        except:
            return jsonify(status='error')
        return jsonify(status='ok')


class SuggestView(MethodView):

    decorators = [authenticated]

    def get(self):
        items = db.session\
            .query(Item.name, sa.func.count(Item.name).label('count'))\
            .group_by(Item.name)\
            .all()
        return jsonify(suggestions=[dict(count=item.count, name=item.name)
                                    for item in items])


item = ItemView.as_view('item')
login = LoginView.as_view('login')
status = StatusView.as_view('status')
suggest = SuggestView.as_view('suggest')
