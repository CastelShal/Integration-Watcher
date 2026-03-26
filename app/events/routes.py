from flask import Blueprint, request, jsonify
from app.extensions import mongo
from datetime import datetime, timedelta
from bson import ObjectId
import logging

logger = logging.getLogger("event_logger")
events = Blueprint('events', __name__, url_prefix='/event')

@events.route('', methods=['GET'])
def get_events():
    """
    Process GET requests to fetch events from the MongoDB collection. It supports an optional query parameter 'mongoId' to fetch only documents added after the specified ID. Additionally, it filters events to include only those that were added within the last 15 seconds. The results are returned as a JSON response.
    Returns:
        A JSON response containing a list of events that match the query criteria
    """
    try:
        query = {}
        # Get the mongoId query parameter
        last_id = request.args.get('mongoId', None)
        
        # If mongoId is provided, get only documents added after it
        if last_id:
            query['_id'] = {'$gt': ObjectId(last_id)}
        
        # Only fetch events within the last 15 seconds
        fifteen_seconds_ago = datetime.utcnow() - timedelta(seconds=15)
        query['timestamp'] = {'$gte': fifteen_seconds_ago}
        logger.info(f'Querying database with criteria: {query}')

        # Query the database
        documents = mongo.db["webhooks"].find(query)
        events_dict = list(map(dict, documents))
        logger.info(f'Fetched {len(events_dict)} events from the database with results: {events_dict}')

        return jsonify(events_dict), 200
    
    except Exception as e:
        logger.exception("Error fetching events: %s")
        return jsonify({'error': 'Internal server error'}), 500
