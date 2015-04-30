import json

from application.models import User


class TestLogin():

    def test_post(self, db, client):
        user = User(username='tester', password='tester')
        db.session.add(user)
        db.session.commit()
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(dict(username='tester', password='tester'))
        resp = client.post('/login', headers=headers, data=data)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 200

    def test_post_forbidden(self, db, client):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'incorrect': 'data'})
        resp = client.post('/login', headers=headers, data=data)
        assert resp.headers.get('Content-Type') == 'application/json'
        assert resp.status_code == 403
