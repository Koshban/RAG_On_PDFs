from app.web import create_app

flask_app, celery_app = create_app()
#flask_app, celery_app = create_app()
celery_app = flask_app.extensions["celery"]
