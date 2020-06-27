class quizWiki:

    CREATE_BLOCK = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "`/quiz start` : Starts Quiz Creation Prompt"
			}
		}

    HELP_BLOCK = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "`/quiz help`: List quiz commands"
			}
		}
    
    def __init__(self, channel):
        self.channel = channel
        self.username = "pythonboardingbot"
        self.icon_emoji = ":robot_face:"

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks":[
                self.CREATE_BLOCK,
                self.HELP_BLOCK
            ]
        }


