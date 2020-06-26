import requests
from .displayconfimation import displayConfirmation
import json



def sendConfirmation(url,channel):
    
    confirmation = displayConfirmation(channel)

    message = confirmation.get_message_payload()

    response = requests.post(url,data=json.dumps(message))