import requests

def init_chat_history(chat_id, system_message):
    messages =[system_message]
    requests.post(
        "https://eu-central-1.aws.data.mongodb-api.com/app/data-ienxugs/endpoint/data/v1/action/insertOne",
        json={
            "collection": "chat_history",
            "database": "VPU29",
            "dataSource": "Cluster0",
            "document": {
                "chat_id": chat_id,
                "messages": messages, }
        },
        headers={'api-key': 'R5PeVST4qP0xcGmWYFmWlWC4m5Ofy4eD3IoHf7gk5SVAHPihj1hF1H1NB1M5nHqk'},
    )
    return messages

def get_chat_history(chat_id):
    response = requests.post(
        "https://eu-central-1.aws.data.mongodb-api.com/app/data-ienxugs/endpoint/data/v1/action/findOne",
        json={
            "collection": "chat_history",
            "database": "VPU29",
            "dataSource": "Cluster0",
            "filter": {
                "chat_id": chat_id
                },
                "projection": {
                "messages": 1,
                }
        },
        headers={'api-key': 'R5PeVST4qP0xcGmWYFmWlWC4m5Ofy4eD3IoHf7gk5SVAHPihj1hF1H1NB1M5nHqk'},
    )
    if response.json()["document"] == None:
        return None
    return response.json()["document"]["messages"]


def append_chat_history(chat_id, message):
    requests.post(
        "https://eu-central-1.aws.data.mongodb-api.com/app/data-ienxugs/endpoint/data/v1/action/updateMany",
        json={
            "collection": "chat_history",
            "database": "VPU29",
            "dataSource": "Cluster0",
            "filter": {
                "chat_id": chat_id
            },
            "update": {
                "$push": {"messages": message}
            },
            "upsert": False
        },
        headers={'api-key': 'R5PeVST4qP0xcGmWYFmWlWC4m5Ofy4eD3IoHf7gk5SVAHPihj1hF1H1NB1M5nHqk'},
    )
    return get_chat_history(chat_id)

