import os
from flask import Flask

from application.views import login
from application.errors import init_errors
from application.models import init_models


def make_app(config={}):
    app = Flask(__name__)
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL'),
    })
    app.config.update(config)

    init_errors(app)
    init_models(app)

    routes = {'/login': login}

    for endpoint, func in routes.iteritems():
        app.add_url_rule(endpoint, view_func=func)

    return app


app = make_app()
