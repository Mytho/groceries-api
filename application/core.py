from __future__ import absolute_import
from flask import Flask

from application.views import login


app = Flask(__name__)
routes = {'/login': login}

for endpoint, func in routes.iteritems():
    app.add_url_rule(endpoint, view_func=func)
