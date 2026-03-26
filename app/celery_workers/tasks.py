import os

import hmac
import hashlib
from json.decoder import JSONDecoder
from celery.signals import worker_process_init
from pymongo import MongoClient
from .event_parser import process_event
from .config import celery

def validate_signature(payload, signature):
    """
    Validate the authenticity of a GitHub webhook request using HMAC module
    Args:
        payload (bytes): The raw request payload from GitHub webhook.
        signature (str): The signature from the GitHub webhook header (format: 'sha256=<hex>').
    Returns:
        bool: True if the signature is valid and matches the expected HMAC, False otherwise.
    """
    secret = os.getenv("GITHUB_SECRET").encode()
    mac = hmac.new(secret, msg=payload, digestmod=hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)

@worker_process_init.connect
def init_mongo(**kwargs):
    global client
    client = MongoClient(
        os.getenv("MONGO_URI"),
    )

@celery.task()
def handle_event(req_data, signature, event_type):
    """
    Process incoming GitHub webhook events and store validated data in MongoDB.
    Args:
        req_data (bytes): The raw request body from the GitHub webhook.
        signature (str): The signature from the GitHub webhook header for validation.
        event_type (str): The type of GitHub event (e.g., 'push', 'pull_request').
    Returns:
        None
    """
    if not validate_signature(req_data, signature):
        return None
    # TO-DO possibly throw error 

    parsed_data = JSONDecoder().decode(req_data.decode('utf-8'))
    processed = process_event(event_type, parsed_data)
    if processed is None:
        print("This data is not processable")
    else:
        res = client.get_default_database().get_collection("webhooks").insert_one(processed)
        print(f"Event parsed with event type: {event_type} with ack {res.acknowledged} and insertion id {res.inserted_id}")
