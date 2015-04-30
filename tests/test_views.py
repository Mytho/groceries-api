import json

from application.models import encode_token


def test_authenticated_forbidden(client):
    headers = {'Content-Type': 'applicaton/json'}
    resp = client.get('/item', headers=headers)
    assert resp.headers.get('Content-Type') == 'application/json'
    assert resp.status_code == 403


class TestItem():

    def test_get(self, client, user):
        headers = {'Content-Type': 'application/json',
                   'X-Auth-Token': encode_token(dict(id=user.id))}
        resp = client.get('/item', headers=headers)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 200


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
