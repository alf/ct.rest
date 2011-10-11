from __future__ import absolute_import
import datetime
from decimal import Decimal

from flask import jsonify
from flask import url_for
from flask import request
from flask import g

from .auth import requires_auth
from .dates import get_next_week, get_prev_week
from .dates import get_next_month, get_prev_month
from .dates import get_next_day, get_prev_day
from ct.core.activity import Activity


def get_template_url(name):
    m = {
        '<year>': '11111',
        '<month>': '22222',
        '<day>': '33333',
        '<week>': '44444',
    }

    if name == '.week':
        url = url_for('.week', year=m.get("<year>"), week=m.get("<week>"))
    elif name == '.month':
        url = url_for('.month', year=m.get("<year>"), month=m.get("<month>"))
    elif name == '.day':
        url = url_for('.day', year=m.get("<year>"),
                      month=m.get("<month>"), day=m.get("<day>"))
    else:
        raise NotImplementedError(
            "Don't know how to create template for %s" % name)

    for template, placeholder in m.items():
        url = url.replace(placeholder, template)

    return url


@requires_auth
def index():
    return jsonify({
        "description": "REST API for CT version 1.0",
        "links": [{
                    "rel": "available-projects",
                    "href": url_for('.projects')
        }, {
                    "rel": "activities-by-week",
                    "href": get_template_url(".week")
        }, {
                    "rel": "activities-by-month",
                    "href": get_template_url(".month")
        }, {
                    "rel": "activities-by-day",
                    "href": get_template_url(".day")
        }]
    })


def serialize_projects(projects):
    result = []
    for p in projects:
        result.append({
            'id': p.id,
            'name': p.name,
            'project_name': p.project_name,
            'task_name': p.task_name,
            'subtask_name': p.subtask_name,
            'activity_name': p.activity_name,
        })
    return result


def serialize_activities(activities):
    result = []
    for activity in activities:
        if activity.duration <= 0:
            continue

        result.append({
                'id': activity.project_id,
                'comment': activity.comment,
                'duration': str(activity.duration),
                'day': activity.day.strftime("%Y-%m-%d")
        })
    return result


@requires_auth
def get_projects():
    projects = serialize_projects(g.ct.get_projects())

    return jsonify({
            "projects": projects
    })


def get_next_week_url(year, week):
    y, w = get_next_week(year, week)
    return url_for(".week", year=y, week=w)


def get_prev_week_url(year, week):
    y, w = get_prev_week(year, week)
    return url_for(".week", year=y, week=w)


@requires_auth
def get_week(year, week):
    activities = serialize_activities(g.ct.get_week(year, week))

    return jsonify({
            "activities": activities,
            "links": [{
                    "rel": "next-week",
                    "href": get_next_week_url(year, week)
            }, {
                    "rel": "prev-week",
                    "href": get_prev_week_url(year, week)
            }]
    })


def get_next_month_url(year, month):
    y, m = get_next_month(year, month)
    return url_for(".month", year=y, month=m)


def get_prev_month_url(year, month):
    y, m = get_prev_month(year, month)
    return url_for(".month", year=y, month=m)


@requires_auth
def get_month(year, month):
    activities = serialize_activities(g.ct.get_month(year, month))

    return jsonify({
            "activities": activities,
            "links": [{
                    "rel": "next-month",
                    "href": get_next_month_url(year, month)
            }, {
                    "rel": "prev-month",
                    "href": get_prev_month_url(year, month)
            }]
    })


def get_next_day_url(year, month, day):
    y, m, d = get_next_day(year, month, day)
    return url_for(".month", year=y, month=m, day=d)


def get_prev_day_url(year, month, day):
    y, m, d = get_prev_day(year, month, day)
    return url_for(".month", year=y, month=m, day=d)


def get_day(year, month, day):
    activities = serialize_activities(g.ct.get_day(year, month, day))

    return jsonify({
            "activities": activities,
            "links": [{
                    "rel": "next-day",
                    "href": get_next_day_url(year, month, day)
            }, {
                    "rel": "prev-day",
                    "href": get_prev_day_url(year, month, day)
            }]
    })


def set_day(year, month, day):
    current_activities = g.ct.get_day(year, month, day)
    to_add = request.json['activities']
    to_delete = [x for x in current_activities if not x in to_add]

    for data in to_add:
        activity = activity_from_dict(data)
        g.ct.report_activity(activity)

    for data in to_delete:
        data['duration'] = 0
        activity = activity_from_dict(data)
        g.ct.report_activity(activity)

    return get_day(year, month, day)


@requires_auth
def day(year, month, day):
    if request.method == "GET":
        return get_day(year, month, day)
    if request.method == "PUT":
        return set_day(year, month, day)
    raise NotImplementedError(
        "Don't know how to handle method %s" % request.method)


def activity_from_dict(data):
    year, month, day = [int(x) for x in data['day'].split("-")]
    date = datetime.date(year, month, day)
    duration = Decimal(data['duration'])
    return Activity(date, data['id'], duration, data['comment'])


def add_routes(api):
    root = 'v1_0'
    api.add_url_rule('/v1/',
                     root + '.index', index)
    api.add_url_rule('/v1/projects/',
                     root + '.projects', get_projects)
    api.add_url_rule('/v1/week/<int:year>/<int:week>',
                     root + '.week', get_week)
    api.add_url_rule('/v1/month/<int:year>/<int:month>',
                     root + '.month', get_month)
    api.add_url_rule('/v1/day/<int:year>/<int:month>/<int:day>',
                     root + '.day', day, methods=["GET", "PUT"])
