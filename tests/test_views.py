import json
import sqlalchemy as sa
from mock import patch

from application.models import Item


def test_authenticated_forbidden(client):
    client.open('get', '/item', assert_status_code=403)


class TestItem():

    def test_get(self, client, user, items):
        item = items.pop()
        resp = client.open('get', '/item/{}'.format(item.id), user=user)
        assert json.loads(resp.data.decode('utf-8')) == item.as_dict()

    def test_get_not_found(self, client, user):
        client.open('get', '/item/{}'.format(99999), user=user,
                    assert_status_code=404)

    def test_get_all(self, client, user, items):
        resp = client.open('get', '/item', user=user)
        for item in items:
            assert item.as_dict() in json.loads(resp.data.decode('utf-8'))\
                                         .get('items', [])

    def test_post(self, client, user):
        resp = client.open('post', '/item',
                           data=json.dumps(dict(name='zucchini')), user=user)
        data = resp.data.decode('utf-8')
        assert json.loads(data).get('id') > 0
        assert json.loads(data).get('name') == 'zucchini'
        assert json.loads(data).get('is_bought') is False

    def test_post_empty(self, client, user):
        resp = client.open('post', '/item', user=user, assert_status_code=400)
        assert resp.status_code == 400

    def test_put(self, client, user, items):
        item = items.pop()
        assert item.is_bought is False
        resp = client.open('put', '/item/{}'.format(item.id), user=user)
        assert json.loads(resp.data.decode('utf-8')).get('is_bought') is True

    def test_put_not_found(self, client, user):
        client.open('put', '/item/{}'.format(99999), user=user,
                    assert_status_code=404)

    def test_put_empty(self, client, user):
        client.open('put', '/item', user=user, assert_status_code=400)

    def test_delete(self, client, user, items):
        item = items.pop()
        client.open('delete', '/item/{}'.format(item.id), user=user)
        assert item not in Item.query.all()

    def test_delete_not_found(self, client, user):
        client.open('delete', '/item/{}'.format(99999), user=user,
                    assert_status_code=404)

    def test_delete_empty(self, client, user):
        client.open('delete', '/item', user=user, assert_status_code=400)


class TestLogin():

    def test_post(self, client, user):
        data = json.dumps(dict(username=user.username,
                               password=user.plaintext_password))
        client.open('post', '/login', data=data)

    def test_post_forbidden(self, client):
        data = json.dumps({'incorrect': 'data'})
        client.open('post', '/login', data=data, assert_status_code=403)


class TestStatus():

    def test_get(self, client):
        client.open('get', '/status')

    @patch('application.models.db.session.query',
           return_value=sa.exc.TimeoutError('Connection timed out'))
    def test_get_exception(self, patched_method, client):
        client.open('get', '/status')
        assert patched_method.call_count == 1


class TestSuggest():

    def test_get(self, client, user):
        client.open('get', '/suggest', user=user)
