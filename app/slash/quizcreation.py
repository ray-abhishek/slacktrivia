class quizCreation:

    HEADING_BLOCK={
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Quiz creation criteria",
				"emoji": True
			}
		}
    
    DIVIDER_BLOCK={
			"type": "divider"
		}

    SUBMIT_BLOCK={
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Submit",
						"emoji": True
					},
                    "style": "primary",
					"value": "SUBMITBTN"
				}
			]
		}

    CHANNEL_BLOCK={
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Select Channel to start quiz"
			},
			"accessory": {
					"type": "channels_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Select a channel",
						"emoji": True
					}
				}
			}

    def __init__(self, channel, category_list):
        self.channel = channel
        self.username = "pythonboardingbot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.category = category_list

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks":[
                self.HEADING_BLOCK,
                self.DIVIDER_BLOCK,
                self.get_category_block(),
                self.CHANNEL_BLOCK,
                self.get_timespan_block(),
                self.DIVIDER_BLOCK,
                self.SUBMIT_BLOCK
            ]
        }

    
    def create_select_block(self,array,length,block_title,select_title):
        
        options=[]

        for x in range(length):
            obj={}
            obj["text"]={
                "type":"plain_text",
                "text":str(array[x]),
                "emoji":True
            }
            obj["value"]=str(array[x])
            options.append(obj)

        
        return {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": block_title
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": select_title,
					"emoji": True
				},
				"options":options
			}
		}

    def get_category_block(self):

        #category=["Coding","Game Of Thrones","History"]

        length=len(self.category)
        
        block_title="Pick a category for quiz"

        select_title="Select a Category"

        return self.create_select_block(self.category,length,block_title,select_title)
    

    """def get_question_number_block(self):
        questions=[5,10,15]
        length=3
        block_title="Select number of questions for quiz"
        select_title="Select questions"
        return self.create_select_block(questions,length,block_title,select_title)
    """
    
    def get_timespan_block(self):
        time=["3 min","5 min","10 min"]

        length=3

        block_title ="Select time span of the quiz"

        select_title ="Select time"

        return self.create_select_block(time,length,block_title,select_title)
