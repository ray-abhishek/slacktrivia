
class factPayload:

    def __init__(self, channel, fact):
        self.channel = channel
        self.username = "QuizTopia"
        self.icon_emoji = ":robot_face:"
        self.fact = fact

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks":[
                self.init_fact()
            ]
        }

    def init_fact(self):
        return {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Did You know :question: \n> "+self.fact
			}
		}

