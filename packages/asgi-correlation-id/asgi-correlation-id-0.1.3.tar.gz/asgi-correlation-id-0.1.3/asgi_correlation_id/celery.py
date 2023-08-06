from typing import Any
from uuid import uuid4

from celery import Task
from celery.signals import before_task_publish, task_postrun, task_prerun

from asgi_correlation_id.context import celery_current_id, celery_parent_id, correlation_id
from asgi_correlation_id.sentry import set_transaction_id


def configure_celery(
    uuid_length: int = 32,
    log_parent: bool = True,
    parent_header: str = 'CELERY_PARENT_ID',
    correlation_id_header: str = 'CORRELATION_ID',
) -> None:
    """
    Configure Celery event hooks.

    Passes correlation IDs from parent processes to child processes in a Celery context.

    This means a correlation ID can be transferred from a request to a worker, or from a worker to another worker.

    For workers executing scheduled tasks, a correlation ID is generated for each new task.
    """

    @before_task_publish.connect
    def publish_task_from_worker_or_request(headers: dict, **kwargs: Any) -> None:
        """
        Transfer correlation ID from request thread to Celery worker, by adding
        it as a header.

        This way we're able to correlated work executed by Celery workers, back
        to the originating request (if there was one).
        """
        id_value = correlation_id.get()
        headers[correlation_id_header] = id_value

        if log_parent:
            current = celery_current_id.get()
            if current:
                headers[parent_header] = current

    @task_prerun.connect
    def worker_prerun(task: Task, **kwargs: Any) -> None:
        """
        Set request ID, current ID, and parent ID if state was transferred.
        """
        id_value = task.request.get(correlation_id_header)

        if id_value:
            correlation_id.set(id_value)
            set_transaction_id(id_value)
        else:
            generated_correlation_id = uuid4().hex[:uuid_length]
            correlation_id.set(generated_correlation_id)
            set_transaction_id(generated_correlation_id)

        if log_parent:
            origin = task.request.get(parent_header)

            if origin:
                celery_parent_id.set(origin)

            generated_current_id = uuid4().hex[:uuid_length]
            celery_current_id.set(generated_current_id)

    @task_postrun.connect
    def clean_up(_: Task, **kwargs: Any) -> None:
        """
        Clear the context vars, to avoid re-using values in the next task.
        """
        correlation_id.set(None)
        if log_parent:
            celery_current_id.set(None)
            celery_parent_id.set(None)
