from __future__ import absolute_import

from flask import Blueprint
from flask import jsonify
from flask import url_for

from .auth import requires_auth
from . import v1

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return jsonify({
        "description": "REST API for CT",
        "links": [{
                    "rel": "api-version-1.0",
                    "href": url_for(".v1_index", _external=True)
        }, {
                    "rel": "latest",
                    "href": url_for(".v1_index", _external=True)
        }]
    })

v1.add_routes(api)
