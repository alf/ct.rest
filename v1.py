from .auth import requires_auth
from flask import jsonify
from flask import url_for


@requires_auth
def index():
    return jsonify({
        "description": "REST API for CT version 1.0",
        "links": [{
                    "rel": "available-projects",
                    "href": url_for('.projects')
        }, {
                    "rel": "activities-by-week",
                    "href": url_for('.week', year="<year>", week="<week>")
        }]
    })


@requires_auth
def get_projects():
    return jsonify({
            "projects": [
            ]
    })


@requires_auth
def get_week(year, week):
    return jsonify({
            "activities": [
            ]
    })


def add_routes(api):
    root = 'v1_0'
    api.add_url_rule('/v1/', root + '.index', index)
    api.add_url_rule('/v1/projects/', root + '.projects', get_projects)
    api.add_url_rule('/v1/week/<year>/<week>', root + '.week', get_week)
