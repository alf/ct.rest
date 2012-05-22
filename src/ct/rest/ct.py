from __future__ import absolute_import

import datetime
from decimal import Decimal
from flask import g

from ct.core.activity import Activity
from . import dates


def get_current_day():
    y, m, d = dates.get_current_day()
    return get_day(y, m, d)


def get_day(year, month, day):
    return serialize_activities(g.ct.get_day(year, month, day))


def set_day(year, month, day, data):
    current_activities = g.ct.get_day(year, month, day)
    to_delete = [x for x in current_activities if not x in data]

    for row in data:
        activity = activity_from_dict(row)
        g.ct.report_activity(activity)

    for row in to_delete:
        data['duration'] = 0
        activity = activity_from_dict(row)
        g.ct.report_activity(activity)


def get_projects():
    return serialize_projects(g.ct.get_projects())


def get_week(year, week):
    return serialize_activities(g.ct.get_week(year, week))


def get_month(year, month):
    return serialize_activities(g.ct.get_month(year, month))


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


def activity_from_dict(data):
    year, month, day = [int(x) for x in data['day'].split("-")]
    date = datetime.date(year, month, day)
    duration = Decimal(data['duration'])
    return Activity(date, data['id'], duration, data['comment'])
