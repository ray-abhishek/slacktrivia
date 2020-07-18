class quizCustomDisplay:

    DIVIDER_BLOCK =	{
			"type": "divider"
	}


    def __init__(self,trigger_id,category_list):
        self.trigger_id = trigger_id
        self.category_list = category_list

    def get_message_payload(self):
        return {
            "trigger_id":self.trigger_id,
            "view": {
                "type": "modal",
                "title": {
                    "type": "plain_text",
                    "text": "QuizBot",
                    "emoji": True
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Submit",
                    "emoji": True
                },
                "close": {
                    "type": "plain_text",
                    "text": "Cancel",
                    "emoji": True
                },
                "blocks":[
                    self.DIVIDER_BLOCK,
                    self.category_block(),
                    self.create_input_block("Write your question"),
                    self.create_input_block("CORRECT ANSWER"),
                    self.create_input_block("Option 2"),
                    self.create_input_block("Option 3"),
                    self.create_input_block("Option 4"),
                    self.create_time_limit_block(),
                    self.channel_select_block()
                ]
            }
        }

    def create_select_block(self,array,title):
        
        length = len(array)

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
			"type": "input",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a option",
					"emoji": True
				},
            "options":options
            },
            "label": {
                "type": "plain_text",
                "text": title,
                "emoji": True
            }
        }

    def create_time_limit_block(self):
        time=["30 seconds","1 min","2 min"]

        return self.create_select_block(time,"Time Limit for quiz")

    def category_block(self):
        return self.create_select_block(self.category_list,"Category for quiz")

    def create_input_block(self,title):
        return {
			"type": "input",
			"element": {
				"type": "plain_text_input"
			},
			"label": {
				"type": "plain_text",
				"text": title,
				"emoji": True
			}
		}
    
    def channel_select_block(self):
        return {
            "type": "actions",
            "elements": [
                {
                "type": "channels_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select Channel",
                    "emoji": True
                }
                }
            ]
        }

    