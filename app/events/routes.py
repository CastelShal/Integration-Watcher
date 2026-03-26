from flask import Blueprint, request, jsonify
from app.extensions import mongo
from datetime import datetime, timedelta
from bson import ObjectId

events = Blueprint('events', __name__, url_prefix='/event')

@events.route('', methods=['GET'])
def get_events():
    try:
        # Get the mongoId query parameter
        last_id = request.args.get('mongoId', None)
        
        # Build the query
        query = {}
        
        # If mongoId is provided, add the greater than check
        if last_id:
            try:
                query['_id'] = {'$gt': ObjectId(last_id)}
            except Exception:
                return jsonify({'error': 'Invalid mongoId format'}), 400
        
        # Add timestamp filter for documents within the last 15 seconds
        fifteen_seconds_ago = datetime.utcnow() - timedelta(seconds=15)
        # query['timestamp'] = {'$gte': fifteen_seconds_ago}
        
        # Query the database
        documents = list(mongo.db["webhooks"].find(query))
        
        # Transform documents to exclude _id field for JSON response
        events_list = []
        for doc in documents:
            doc_copy = dict(doc)
            doc_copy['_id'] = str(doc_copy['_id'])  # Convert ObjectId to string for JSON serialization
            events_list.append(doc_copy)
        
        return jsonify(events_list), 200
    
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
