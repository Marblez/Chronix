import json

import requests

# used to post messages to discord

def callWebhook(message, discordApi):
    data = {}
    data["content"] = message
    data["username"] = "PaperBot"
    result = requests.post(discordApi, data=json.dumps(data), headers={"Content-type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    
