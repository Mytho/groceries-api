import json

from application.core import app


class TestLogin():

    def test_post(self):
        with app.app_context():
            client = app.test_client()
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({'username': 'tester'})
            resp = client.post('/login', headers=headers, data=data)
            assert resp.headers.get('Content-Type') == 'application/json'
            assert resp.status_code == 200

    def test_post_forbidden(self):
        with app.app_context():
            client = app.test_client()
            headers = {'Content-Type': 'application/json'}
            data = json.dumps({'incorrect': 'data'})
            resp = client.post('/login', headers=headers, data=data)
            assert resp.headers.get('Content-Type') == 'application/json'
            assert resp.status_code == 403
