import os
from flask import Blueprint, json, request
from app.webhook.event_handlers import process_event
from app.extensions import mongo
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    processed = process_event(event_type, data)
    if processed is None:
        return {}, 400
    print(processed)    
    mongo.db["webhooks"].insert_one(processed)
    return {}, 200

@webhook.get('/')
def index():
    return {}, 200
