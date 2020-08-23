import json

import requests

# used to post messages to discord
discordApi = "https://discord.com/api/webhooks/745791613988634697/aquC2D2GHGU70zvvu_gZ_Gsn1ffxHBjzIiodpS7frc5-yLUyxLB3SVbWE7aGauUZ7zhK"

def callWebhook(message):
    data = {}
    data["content"] = message
    data["username"] = "PaperBot"
    result = requests.post(discordApi, data=json.dumps(data), headers={"Content-type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    
