from flask import Blueprint
from flask import jsonify

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return jsonify(
        "description": "REST API for CT",
        "version": "1.0"
    )
