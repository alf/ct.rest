from __future__ import absolute_import

from flask import jsonify
from flask import url_for
from flask import g

from .auth import requires_auth
from .weeks import get_next_week, get_prev_week


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


def add_routes(api):
    root = 'v1_0'
    api.add_url_rule('/v1/',
                     root + '.index', index)
    api.add_url_rule('/v1/projects/',
                     root + '.projects', get_projects)
    api.add_url_rule('/v1/week/<int:year>/<int:week>',
                     root + '.week', get_week)
