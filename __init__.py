from __future__ import absolute_import

from flask import Blueprint
from flask import jsonify
from flask import url_for

from .auth import requires_auth
from . import v1

api = Blueprint('api', __name__)

@api.route('/')
@requires_auth
def index():
    return jsonify({
        "description": "REST API for CT",
        "links": [{
                    "rel": "api-version-1.0",
                    "href": url_for(".v1_0.index")
        }]
    })

v1.add_routes(api)
