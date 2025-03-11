from npmis.celery import app


# @app.task(bind=True, ignore_result=True, retry_backoff=True)
def task_event_commit(
    self, event_id, actor_app_label=None, actor_model_name=None,
    actor_id=None, action_object_app_label=None,
    action_object_model_name=None, action_object_id=None,
    target_app_label=None, target_model_name=None, target_id=None
):
    pass

