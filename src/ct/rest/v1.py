from __future__ import absolute_import

from flask import jsonify
from flask import request

from .auth import requires_auth
from . import ct
from . import url
from . import dates


@requires_auth
def index():
    return jsonify({
        "description": "REST API for CT version 1.0",
        "current-week": get_current_week_data(),
        "available-projects": get_projects_data(),
        "links": [{
                    "rel": "self",
                    "href": url.get_index()
        }, {
                    "rel": "available-projects",
                    "href": url.get_projects()
        }, {
                    "rel": "current-week",
                    "href": url.get_current_week()
        }]
    })


@requires_auth
def get_current_week():
    if request.method == "PUT":
        year, week = dates.get_current_week()
        ct.set_week(year, week, request.json)

    return jsonify(get_current_week_data())


@requires_auth
def get_projects():
    return jsonify(get_projects_data())


def get_current_week_data():
    year, week = dates.get_current_week()

    if request.method == "PUT":
        ct.set_week(year, week, request.json)

    return get_week_data(year, week)


def get_projects_data():
    return {
        "projects": ct.get_projects(),
        "links": [{
            "rel": "self",
            "href": url.get_projects()
        }]
    }


def get_week_data(year, week):
    return {
            "activities": ct.get_week(year, week),
            "links": [{
                    "rel": "self",
                    "href": url.get_current_week()
            }]
    }


def add_routes(api):
    api.add_url_rule('/v1/',
                     'v1_index', index)
    api.add_url_rule('/v1/projects/',
                     'v1_projects', get_projects)
    api.add_url_rule('/v1/current_week',
                     'v1_current_week', get_current_week, methods=["GET", "PUT"])
