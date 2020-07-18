class QuizDisplay:
    """Constructs the question and options and stores the state of which options were selected."""

    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel, author, time_limit):
        self.channel = channel
        self.username = "QuizTopia"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.question = ""
        self.option1 = ""
        self.option2 = ""
        self.option3 = ""
        self.option4 = ""
        self.answer = ""
        self.submitted = []
        self.author = author 
        self.time_limit = time_limit

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self._get_question_block(),
                self._get_options_block(),
                self.DIVIDER_BLOCK,
                self.get_context()
            ]
        }

    def get_updated_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self._get_question_block(),
                self._get_options_block(),
                self.updated_submitted_users(),
                self.DIVIDER_BLOCK,
                self.get_context()
            ]
        }
    
    def get_timeout_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self._get_question_block(),
                self._get_timeout_options_block(),
                self.updated_submitted_users(),
                self.DIVIDER_BLOCK,
                self.get_context_closed()
            ]
        } 

    #This takes the question string, puts it in JSON Object and returns it.
    def _get_question(self,question):
        return {
            "type": "section",
			"text": {
				"type": "plain_text",
				"text": str(question),
				"emoji": True
			}
        }


    def _build_option(self,option):
        return {
            "type": "button",
			"text": {
					"type": "plain_text",
					"text": str(option),
					"emoji": True
					},
			"value": str(option)
        }

    def _build_timeout_option(self,option):
        return{
                "type": "plain_text",
                "text": "• " + str(option),
                "emoji": True
		}

    #This takes the 4 json option objects, wraps them in the actions type Block Object and returns it.
    def _get_options(self):
        return {
            "type" : "actions",
            "elements" : [self.option1,self.option2,self.option3,self.option4]
        }


    #This returns the question block.
    def _get_question_block(self):
        return self._get_question(self.question)

    #This returns the options block.
    def _get_options_block(self):
        return self._get_options()

    
    def _get_timeout_options_block(self):

        option1 = self._build_timeout_option(self.option1["text"]["text"])
        option2 = self._build_timeout_option(self.option2["text"]["text"])
        option3 = self._build_timeout_option(self.option3["text"]["text"])
        option4 = self._build_timeout_option(self.option4["text"]["text"])

        return {
                "type": "section",
                "fields":[option1,option2,option3,option4]
            }

    # This init_message is called from run.py and supplied the parameters. Once the questions and options have been initialised, the message payload(get_message_payload) can be used to return Message Object
    def init_message(self,question,op1,op2,op3,op4,op5):
        self.question = question 
        self.option1 = self._build_option(op1) 
        self.option2 = self._build_option(op2) 
        self.option3 = self._build_option(op3) 
        self.option4 = self._build_option(op4) 
        self.answer = self._build_option(op5)


    
    def updated_submitted_users(self):
        
        submitted_users_array = []
        for x in self.submitted:
            submitted_users_array.append("<@"+str(x)+">")

        submitted_users=",".join(submitted_users_array)
        if len(submitted_users_array)>0:
            return  {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": "Submitted :mailbox: : "+submitted_users
			    }
		    }
        else:
            return {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": "Submitted :mailbox: : "+str(0)
			    }
		    }


    def get_context(self):
        return {
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "Created by "+"<@"+str(self.author)+">" + ":sunglasses:"
				},
                {
					"type": "mrkdwn",
					"text": "Quiz closes in *"+self.time_limit+"* :heavy_exclamation_mark:"
				}
			]
		}

    def get_context_closed(self):
        return {
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "Created by "+"<@"+str(self.author)+">" + ":sunglasses:"
				},
                {
					"type": "mrkdwn",
					"text": "Quiz closed :heavy_exclamation_mark:"
				}
			]
		}

    

   