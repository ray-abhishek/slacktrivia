class quizCreation:

    HEADING_BLOCK={
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Quiz creation criteria",
				"emoji": true
			}
		}
    
    DIVIDER_BLOCK={
			"type": "divider"
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
                self.HEADING_BLOCK,
                self.DIVIDER_BLOCK,
                self.get_category_block(),
                self.get_question_number_block(),
                self.get_timespan_block(),
                self.DIVIDER_BLOCK
            ]
        }

    @staticmethod
    def create_select_block(array,length,block_title,select_title):
        
        options=[]

        for x in range(length):
            obj={}
            obj["text"]={
                "type":"plain_text",
                "text":array[x],
                "emoji":true
            }
            obj["value"]="value-"+str(x)
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
					"emoji": true
				},
				"options":options
			}
		}

    def get_category_block(self):

        category=["Coding","Game Of Thrones","History"]

        length=len(category)
        
        block_title="Pick a category for quiz"

        select_title="Select a Category"

        return create_select_block(category,length,block_title,select_title)
    

    def get_question_number_block(self):
        questions=[5,10,15]

        length=3

        block_title="Select number of questions for quiz"

        select_title="Select questions"

        return create_select_block(questions,length,block_title,select_title)

    
    def get_timespan_block(self):
        time=["5 min","10 min","15 min"]

        length=3

        block_title ="Select time span of the quiz"

        select_title ="Select time"

        return create_select_block(time,length,block_title,select_title)