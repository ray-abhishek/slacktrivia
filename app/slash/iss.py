import requests
import json
from .isspayload import issPayload
from slack import WebClient
import os

slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

def satellite(user_info):
    sat_loc = requests.get("https://api.wheretheiss.at/v1/satellites/25544")
    sat_loc = sat_loc.json()
    latitude = sat_loc["latitude"]
    longitude = sat_loc["longitude"]
    
    coordinates = requests.get("https://api.wheretheiss.at/v1/coordinates/"+str(latitude)+","+str(longitude)).json()
    
    if "error" in coordinates:
        message_payload = issPayload(user_info["channel_id"], None, sat_loc["altitude"],sat_loc["velocity"],None)
        message = message_payload.get_error_message_payload()
    else:
        message_payload = issPayload(user_info["channel_id"], coordinates["timezone_id"], sat_loc["altitude"],sat_loc["velocity"],coordinates["map_url"])
        message = message_payload.get_message_payload()
    
    response = slack_web_client.chat_postMessage(**message)
