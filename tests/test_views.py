import json

from application.models import Item, encode_token


def test_authenticated_forbidden(client):
    headers = {'Content-Type': 'applicaton/json'}
    resp = client.get('/item', headers=headers)
    assert resp.headers.get('Content-Type') == 'application/json'
    assert resp.status_code == 403


class TestItem():

    def test_get(self, client, user, items):
        item = items.pop()
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.get('/item/{}'.format(item.id), headers=headers)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 200
        assert json.loads(resp.data) == item.as_dict()

    def test_get_not_found(self, client, user):
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.get('/item/{}'.format(99999), headers=headers)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 404

    def test_get_all(self, client, user, items):
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.get('/item', headers=headers)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 200
        for item in items:
            assert item.as_dict() in json.loads(resp.data).get('items', [])

    def test_post(self, client, user):
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.post('/item', headers=headers,
                           data=json.dumps(dict(name='zucchini')))
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 200
        assert json.loads(resp.data).get('id') > 0
        assert json.loads(resp.data).get('name') == 'zucchini'
        assert json.loads(resp.data).get('is_bought') is False

    def test_put(self, client, user, items):
        item = items.pop()
        assert item.is_bought is False
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.put('/item/{}'.format(item.id), headers=headers)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 200
        assert json.loads(resp.data).get('is_bought') is True

    def test_put_not_found(self, client, user):
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.put('/item/{}'.format(99999), headers=headers)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 404

    def test_delete(self, client, user, items):
        item = items.pop()
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.delete('/item/{}'.format(item.id), headers=headers)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 200
        assert item not in Item.query.all()

    def test_delete_not_found(self, client, user):
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.delete('/item/{}'.format(99999), headers=headers)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 404


class TestLogin():

    def test_post(self, client, user):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(dict(username=user.username,
                               password=user.plaintext_password))
        resp = client.post('/login', headers=headers, data=data)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 200

    def test_post_forbidden(self, client):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'incorrect': 'data'})
        resp = client.post('/login', headers=headers, data=data)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 403


class TestSuggest():

    def test_get(self, client, user):
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.get('/suggest', headers=headers)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 200
