from flask import Blueprint, abort, request
from app.celery_workers.tasks import handle_event
import logging

logger = logging.getLogger("webhook_logger")
logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG for detailed output
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.get('/')
def index():
    """
    Simple route to check if the webhook service is running.
    """
    logger.info("Received request to index route")

    return {}, 200

@webhook.route('/receiver', methods=["POST"])
def receiver():
    """
    Receives POST requests from GitHub webhooks, validates the presence of signature and event type headers and processes the event asynchronously using a Celery task.
    """
    event_type = request.headers.get('X-GitHub-Event')
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature or not event_type:
        logger.warning("Missing signature or event type in the request headers.")
        abort(401)
    
    logger.debug(f"Received event: {event_type} with signature: {signature}")
    try:
        task_id = handle_event.delay(request.data, signature, event_type)
        logger.info(f"Dispatch event '{event_type}' to Celery worker with task ID: {task_id}")
    except Exception as e:
        logger.exception(f"Failed to dispatch event '{event_type}' to Celery worker")
        abort(500)
    
    return {}, 200


