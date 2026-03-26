import hashlib
import hmac
import os
from flask import Blueprint, abort, json, request
from app.extensions import mongo
from app.celery_workers.tasks import handle_event
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

def validate_signature(payload, signature):
    secret = os.getenv("GITHUB_SECRET").encode()
    mac = hmac.new(secret, msg=payload, digestmod=hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)

@webhook.get('/')
def index():
    return {}, 200

@webhook.route('/receiver', methods=["POST"])
def receiver():
    event_type = request.headers.get('X-GitHub-Event')
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature or not event_type:
        abort(401)
    handle_event.delay(request.data, signature, event_type)
    return {}, 200


