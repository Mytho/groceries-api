from mock import Mock
from werkzeug.test import EnvironBuilder

from application.core import app


def test_app():
    environ = EnvironBuilder(method='GET', path='/not-found').get_environ()
    start_response = Mock()
    app(environ, start_response)
    args, kwargs = start_response.call_args
    assert args[0] == '404 NOT FOUND'
