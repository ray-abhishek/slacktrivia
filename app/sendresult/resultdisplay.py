class resultDisplay:
    
    TITLE_BLOCK={
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Result for the Quiz",
				"emoji": True
			}
		}
    
    def __init__(self, channel, answer, user_data):
        self.channel = channel
        self.username = "QuizTopia"
        self.icon_emoji = ":robot_face:"
        self.correct_answer = answer
        self.user_data = user_data


    def get_message_payload(self):
        return {
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks":[
                self.TITLE_BLOCK,
                self.create_correct_answer_block(self.correct_answer),
                self.create_user_block(self.user_data)
            ]
        }

    def create_correct_answer_block(self,answer):
        return {
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Correct Answer: "+str(answer),
				"emoji": True
			}
		}
    
    def create_user_block(self,user_data):
        
        successfull_users_array = []

        for x in user_data:
            successfull_users_array.append("<@"+str(x)+">")

        successfull_users=",".join(successfull_users_array)
        
        return {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Users who answered correctly :trophy: : "+successfull_users
			}
		}
