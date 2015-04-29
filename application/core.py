from __future__ import absolute_import
from flask import Flask

from application.views import login
from application.errors import init_errors


app = Flask(__name__)
init_errors(app)

routes = {'/login': login}

for endpoint, func in routes.iteritems():
    app.add_url_rule(endpoint, view_func=func)
