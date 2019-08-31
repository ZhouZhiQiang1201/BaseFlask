# -*- config: utf-8 -*-
from flask import Blueprint

blue = Blueprint("blue", __name__, url_prefix="/test")  # url_prefix 前缀

from . import test
