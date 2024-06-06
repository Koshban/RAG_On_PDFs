from app.web import create_app
import os

flask_app = create_app()
#celery_app = create_app()
try:
    celery_app = flask_app.extensions["celery"]
except KeyError as e:
    print(f"OS is {os.name}")
    print(f"Key Error : {e}")
    import traceback
    traceback.print_exc()
    exit
except Exception as e:
    print(f"An error occurred : {e}")
    import traceback
    traceback.print_exc()
