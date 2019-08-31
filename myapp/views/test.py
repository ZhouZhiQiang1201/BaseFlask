# -*- config: utf-8 -*-
from flask import jsonify

from myapp.views import blue
from myapp.celery_task.task1 import add_together


@blue.route("/test")
def test_task():
    result = add_together.delay(1, 56)
    result.wait()
    return jsonify({"data": result.wait()})
