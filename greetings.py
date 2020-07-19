class Greetings:

    greetings_block={
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hey, I am QuizTopia. To know my commands , type  `/quiz help`"
			    }
		    }


    def __init__(self, channel):
        self.channel = channel
        self.username = "pythonboardingbot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks":[
                self.greetings_block
            ]
        }
        
