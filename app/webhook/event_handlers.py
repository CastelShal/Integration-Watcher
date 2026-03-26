from datetime import datetime

def process_event(event_type, event_data):
    if event_type == 'push':
        return process_push(event_data)
    elif event_type == 'pull_request':
        if event_data['pull_request']['merged']:
            return process_merge(event_data)
        else:
            return process_pull_request(event_data)

def process_push(event_data):
    req_id = str(event_data['head_commit']["id"])
    pusher = event_data['pusher']['name']
    to_branch = event_data['ref'].split('/')[-1]
    timestamp = datetime.fromisoformat(event_data['head_commit']['timestamp'])
    return {
        "request_id": req_id,
        "action": "PUSH",
        "author": pusher,
        "from_branch": None,
        "to_branch": to_branch,
        "timestamp": timestamp
        }

def process_pull_request(event_data):
    req_id = str(event_data['pull_request']['id'])
    timestamp = datetime.fromisoformat(event_data['pull_request']['created_at'])
    author = event_data['pull_request']['user']['login']
    from_branch = event_data['pull_request']['head']['ref']
    to_branch = event_data['pull_request']['base']['ref']
    return {
        "request_id": req_id,
        "action": "PULL_REQUEST",
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    }

def process_merge(event_data):
    req_id = str(event_data['pull_request']['id'])
    timestamp = datetime.fromisoformat(event_data['pull_request']['merged_at'])
    print(timestamp.isoformat())
    print(event_data['pull_request']['merged_at'])
    author = event_data['pull_request']['user']['login']
    from_branch = event_data['pull_request']['head']['ref']
    to_branch = event_data['pull_request']['base']['ref']
    return {
        "request_id": req_id,
        "action": "MERGE",
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    }