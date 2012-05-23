from __future__ import absolute_import

from flask import url_for


def get_projects():
    return url_for(".v1_projects", _external=True)


def get_current_week():
    return url_for(".v1_current_week", _external=True)


def get_index():
    return url_for(".v1_index", _external=True)
