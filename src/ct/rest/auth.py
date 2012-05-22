from __future__ import absolute_import

from functools import wraps
from hashlib import sha256
from flask import request, Response
from flask import session, g

from ct.core.apis import BaseAPI


def get_ct_object(username, password):
    key = get_session_key(username, password)
    if key in session and session[key].valid_session():
        return session[key]

    if do_ct_login(username, password):
        return get_ct_object(username, password)

    return None


def do_ct_login(username, password):
    ct = BaseAPI("https://currenttime.bouvet.no")
    logged_in = ct.login(username, password)
    if logged_in:
        key = get_session_key(username, password)
        session[key] = ct

    return logged_in


def get_session_key(username, password):
    return sha256("%s:%s" % (username, password)).hexdigest()


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return get_ct_object(username, password) is not None


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

        g.ct = get_ct_object(auth.username, auth.password)

        return f(*args, **kwargs)
    return decorated
