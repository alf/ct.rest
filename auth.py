from functools import wraps
from flask import request, Response


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def get_auth_headers():
    """Returns the WWW-Authenticate headers. We use Basic unless the
    clients has set the UseXBasic header. In that case we use XBasic
    instead. This is because most web browsers insist on showing the
    Basic auth dialogue even if the request is done using XHR."""

    auth_type = "Basic"
    if request.headers.get('UseXBasic'):
        auth_type = "XBasic"

    return {
        'WWW-Authenticate': '%s realm="Login Required"' % auth_type
    }


def authenticate():
    """Sends a 401 response that enables basic auth"""

    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    get_auth_headers())


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
