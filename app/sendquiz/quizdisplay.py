class QuizDisplay:
    """Constructs the question and options and stores the state of which options were selected."""

    #DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "QuizBot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.question = ""
        self.option1 = ""
        self.option2 = ""
        self.option3 = ""
        self.option4 = ""
        self.answer = ""
        self.submitted = []
        #self.reaction_task_completed = False
        #self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                #self.QUESTION_BLOCK,
                #self.DIVIDER_BLOCK,
                self._get_question_block(),
                self._get_options_block(),
                #self.DIVIDER_BLOCK,
            ],
        }

    def get_updated_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                #self.QUESTION_BLOCK,
                #self.DIVIDER_BLOCK,
                self._get_question_block(),
                self._get_options_block(),
                self.updated_submitted_users()
                #self.DIVIDER_BLOCK,
            ],
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

    # This init_message is called from run.py and supplied the parameters. Once the questions and options have been initialised, the message payload(get_message_payload) can be used to return Message Object
    def init_message(self,question,op1,op2,op3,op4,op5):
        self.question = question 
        self.option1 = self._build_option(op1) 
        self.option2 = self._build_option(op2) 
        self.option3 = self._build_option(op3) 
        self.option4 = self._build_option(op4) 
        self.answer = self._build_option(op5)

    # This method takes the correct answer as parameter and accordingly changes the color of the correct option to green, and rest to red. 
    def inform_user(self):
        print("----------------Modifying Color According to Correctness of Option-----------")
        if self.answer==self.option1["value"]:
            self.option1["style"] = "primary"
            self.option2["style"] = "danger"
            self.option3["style"] = "danger"
            self.option4["style"] = "danger"
        elif self.answer==self.option2["value"]:
            self.option1["style"] = "danger"
            self.option2["style"] = "primary"
            self.option3["style"] = "danger"
            self.option4["style"] = "danger"
        elif self.answer==self.option3["value"]:
            self.option1["style"] = "danger"
            self.option2["style"] = "danger"
            self.option3["style"] = "primary"
            self.option4["style"] = "danger"
        elif self.answer==self.option4["value"]:
            self.option1["style"] = "danger"
            self.option2["style"] = "danger"
            self.option3["style"] = "danger"
            self.option4["style"] = "primary"

    
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
            return {}

    """
    #This takes the 4 option strings, put them in a JSON Object and returns it.
    @staticmethod
    def _get_options(option1, option2, option3, option4):
        return {
            "type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": str(option1),
						"emoji": True
					},
					"value": str(option1)
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": str(option2),
						"emoji": True
					},
					"value": str(option2)
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": str(option3),
						"emoji": True
					},
					"value": str(option3),
                    
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": str(option4),
						"emoji": True
					},
					"value": str(option4)"
				}
			]
        }
    """
    

   