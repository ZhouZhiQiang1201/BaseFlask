# -*- coding: utf-8 -*-
import time

from myapp import celery


@celery.task()
def add_together(a, b):
    return a + b


@celery.task(name="import_data")
def import_data():
    print("celery timing {}".format(time.time()))
