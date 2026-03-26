import hashlib
import hmac
import os
from flask import Blueprint, abort, json, request
from app.webhook.event_handlers import process_event
from app.extensions import mongo
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
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        abort(401)
    if not validate_signature(request.data, signature):
        abort(403)

    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    processed = process_event(event_type, data)
    if processed is None:
        return {}, 400
    mongo.db["webhooks"].insert_one(processed)
    return {}, 200

