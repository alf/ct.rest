from __future__ import absolute_import

from flask import url_for

from . import dates


def get_template(name):
    m = {
        '{year}': '11111',
        '{month}': '22222',
        '{day}': '33333',
        '{week}': '44444',
    }

    if name == '.v1_week':
        url = url_for('.v1_week', year=m.get("{year}"),
                      week=m.get("{week}"), _external=True)
    elif name == '.v1_month':
        url = url_for('.v1_month', year=m.get("{year}"),
                      month=m.get("{month}"), _external=True)
    elif name == '.v1_day':
        url = url_for('.v1_day', year=m.get("{year}"),
                      month=m.get("{month}"), day=m.get("{day}"),
                      _external=True)
    else:
        raise NotImplementedError(
            "Don't know how to create template for %s" % name)

    for template, placeholder in m.items():
        url = url.replace(placeholder, template)

    return url


def get_day(year, month, day):
    return url_for(".v1_day", year=year, month=month, day=day, _external=True)


def get_current_day():
    y, m, d = dates.get_current_day()
    return get_day(y, m, d)


def get_next_day(year, month, day):
    y, m, d = dates.get_next_day(year, month, day)
    return get_day(y, m, d)


def get_prev_day(year, month, day):
    y, m, d = dates.get_prev_day(year, month, day)
    return get_day(y, m, d)


def get_week(year, week):
    return url_for(".v1_week", year=year, week=week, _external=True)


def get_current_week():
    y, w = dates.get_current_week()
    return get_week(y, w)


def get_next_week(year, week):
    y, w = dates.get_next_week(year, week)
    return get_week(y, w)


def get_prev_week(year, week):
    y, w = dates.get_prev_week(year, week)
    return get_week(y, w)


def get_week_from_day(year, month, day):
    y, w = dates.get_week_from_day(year, month, day)
    return get_week(y, w)


def get_month(year, month):
    return url_for(".v1_month", year=year, month=month, _external=True)


def get_current_month():
    y, m = dates.get_current_month()
    return get_month(y, m)


def get_next_month(year, month):
    y, m = dates.get_next_month(year, month)
    return get_month(y, m)


def get_prev_month(year, month):
    y, m = dates.get_prev_month(year, month)
    return get_month(y, m)


def get_month_from_week(year, week):
    y, m = dates.get_month_from_week(year, week)
    return get_month(y, m)


def get_projects():
    return url_for(".v1_projects", _external=True)
