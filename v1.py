from __future__ import absolute_import

from flask import jsonify
from flask import request

from .auth import requires_auth
from . import ct
from . import url


@requires_auth
def index():
    return jsonify({
        "description": "REST API for CT version 1.0",
        "activities": ct.get_current_day(),
        "available-projects": ct.get_projects(),
        "links": [{
                    "rel": "available-projects",
                    "href": url.get_projects()
        }, {
                    "rel": "current-day",
                    "href": url.get_current_day()
        }, {
                    "rel": "current-week",
                    "href": url.get_current_week()
        }, {
                    "rel": "current-month",
                    "href": url.get_current_month()
        }, {
                    "rel": "activities-by-week",
                    "href": url.get_template(".v1_week")
        }, {
                    "rel": "activities-by-month",
                    "href": url.get_template(".v1_month")
        }, {
                    "rel": "activities-by-day",
                    "href": url.get_template(".v1_day")
        }]
    })


@requires_auth
def day(year, month, day):
    if request.method == "PUT":
        ct.set_day(year, month, day, request.json['activities'])

    return jsonify({
            "activities": ct.get_day(year, month, day),
            "links": [{
                    "rel": "current",
                    "href": url.get_current_day()
            }, {
                    "rel": "next",
                    "href": url.get_next_day(year, month, day)
            }, {
                    "rel": "prev",
                    "href": url.get_prev_day(year, month, day)
            }, {
                    "rel": "up",
                    "href": url.get_week_from_day(year, month, day)
            }, {
                    "rel": "edit",
                    "href": url.get_day(year, month, day)
            }, {
                    "rel": "self",
                    "href": url.get_day(year, month, day)
            }]
    })


@requires_auth
def week(year, week):
    return jsonify({
            "activities": ct.get_week(year, week),
            "links": [{
                    "rel": "current",
                    "href": url.get_current_week()
            }, {
                    "rel": "next",
                    "href": url.get_next_week(year, week)
            }, {
                    "rel": "prev",
                    "href": url.get_prev_week(year, week)
            }, {
                    "rel": "up",
                    "href": url.get_month_from_week(year, week)
            }]
    })


@requires_auth
def month(year, month):
    return jsonify({
            "activities": ct.get_month(year, month),
            "links": [{
                    "rel": "current",
                    "href": url.get_current_month()
            }, {
                    "rel": "next",
                    "href": url.get_next_month(year, month)
            }, {
                    "rel": "prev",
                    "href": url.get_prev_month(year, month)
            }]
    })


@requires_auth
def projects():
    return jsonify({
            "projects": ct.get_projects()
    })


def add_routes(api):
    api.add_url_rule('/v1/',
                     'v1_index', index)
    api.add_url_rule('/v1/projects/',
                     'v1_projects', projects)
    api.add_url_rule('/v1/week/<int:year>/<int:week>',
                     'v1_week', week)
    api.add_url_rule('/v1/month/<int:year>/<int:month>',
                     'v1_month', month)
    api.add_url_rule('/v1/day/<int:year>/<int:month>/<int:day>',
                     'v1_day', day, methods=["GET", "PUT"])
