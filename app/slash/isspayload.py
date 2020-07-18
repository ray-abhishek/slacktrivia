import math

class issPayload:
    WARNING_BLOCK = 		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": " :warning: We are facing difficulties in fetching current location, please try again later.",
					"emoji": True
				}
			]
	}

    def __init__(self, channel, location, altitude, velocity, link):
        self.channel = channel
        self.username = "QuizTopia"
        self.icon_emoji = ":robot_face:"
        self.location = location
        self.altitude = str(math.ceil(altitude))+" km"
        self.velocity = str(math.ceil(velocity))+" km/h"
        self.link = link

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks":[
                self.init_iss(),
                self.init_map()
            ]
        }
    
    def get_error_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks":[
                self.init_error(),
                self.WARNING_BLOCK
            ]
        }

    def init_error(self):
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":satellite: ISS is currently flying at a speed :rocket: of "+str(self.velocity) +" at an altitude of " +str(self.altitude) +"."
            }
        }

    def init_iss(self):
        return {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":satellite: ISS is currently flying over "+str(self.location) + " at a speed :rocket: of "+str(self.velocity) +" at an altitude of " +str(self.altitude) +"."
			}
		}
    
    def init_map(self):
        return {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": str(self.link)
			}
	    }