from flask import Flask


def create_app(config):
    app = Flask('tamarack')

    configure_app(app, config)
    configure_blueprints(app)
    configure_db(app)
    configure_celery(app)

    return app


def configure_app(app, config):
    app.config.from_pyfile('settings/defaults.py')
    app.config.from_pyfile(config)


def configure_blueprints(app):
    from tamarack.receiverapi.views import receiverapi
    from tamarack.explorerapi.views import explorerapi
    from tamarack.explorerweb.views import explorerweb

    app.register_blueprint(receiverapi, url_prefix='/receiver-api/v1')
    app.register_blueprint(explorerapi, url_prefix='/explorer-api/v1')
    app.register_blueprint(explorerweb, url_prefix='/')


def configure_db(app):
    from .db import db

    db.init_app(app)


def configure_celery(app):
    from .celery import celery

    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
