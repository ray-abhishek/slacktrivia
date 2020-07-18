class displayConfirmation:
    
    def __init__(self,channel):
        self.channel = channel
        self.username = "QuizTopia"
        self.icon_emoji = ":robot_face:"

    
    def get_message_payload(self):
        return {
            "text":"Confirmation",
            "replace_original": "true",
            "blocks":[
                self.message_block()
            ]
        }

    def message_block(self):
        return {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "The quiz has been created successfully in <#"+str(self.channel)+">"
			}
		}