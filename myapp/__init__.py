# -*- coding: utf-8 -*-

import os

import click
from flask import Flask, render_template
from flask_mail import Mail

from myapp.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

mail = Mail()
from celery import Celery


class MyCelery(Celery):

    def __init__(self, *args, **kwargs):
        self.init_app(*args, **kwargs)

    def init_app(self, *args, **kwargs):
        super(MyCelery, self).__init__(*args, **kwargs)


celery = MyCelery()


def create_app(config_name=None):
    # 设置默认开发环境
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'dev')

    app = Flask(__name__)
    # 获取配置文件
    app.config.from_object(config[config_name])

    register_blueprints(app)
    # 注册celery
    register_celery(app)
    return app


def register_extensions(app):
    mail.init_app(app)


def register_celery(app):
    celery.init_app(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def register_blueprints(app):
    """注册蓝图"""
    from myapp.views import blue
    app.register_blueprint(blue)


def register_shell_context(app):
    """在shell直接调用"""
    pass
    # @app.shell_context_processor
    # def make_shell_context():
    #     return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_errors(app):
    """处理异常"""

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # @app.errorhandler(CSRFError)
    # def handle_csrf_error(e):
    #     return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    """注册命令"""

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        pass
        """Initialize the database."""
        # if drop:
        #     click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        #     db.drop_all()
        #     click.echo('Drop tables.')
        # db.create_all()
        # click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""
        pass
        # click.echo('Initializing the database...')
        # db.create_all()
        # pass
