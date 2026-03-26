from flask import Blueprint, request, jsonify
from app.extensions import mongo
from datetime import datetime, timedelta
from bson import ObjectId

events = Blueprint('events', __name__, url_prefix='/event')

@events.route('', methods=['GET'])
def get_events():
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

        # Query the database
        documents = mongo.db["webhooks"].find(query, {'_id': 0})
        events_dict = list(map(dict, documents))

        return jsonify(events_dict), 200
    
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
