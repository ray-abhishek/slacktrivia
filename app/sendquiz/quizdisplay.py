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
    def init_message(self,question,op1,op2,op3,op4):
        self.question = question 
        self.option1 = self._build_option(op1) 
        self.option2 = self._build_option(op2) 
        self.option3 = self._build_option(op3) 
        self.option4 = self._build_option(op4) 

    # This method takes the correct answer as parameter and accordingly changes the color of the correct option to green, and rest to red. 
    def inform_user(self, answer):
        if answer==self.option1["text"]["text"]:
            self.option1["style"] = "primary"
            self.option2["style"] = "danger"
            self.option3["style"] = "danger"
            self.option4["style"] = "danger"
        elif answer==self.option2["text"]["text"]:
            self.option1["style"] = "danger"
            self.option2["style"] = "primary"
            self.option3["style"] = "danger"
            self.option4["style"] = "danger"
        elif answer==self.option3["text"]["text"]:
            self.option1["style"] = "danger"
            self.option2["style"] = "danger"
            self.option3["style"] = "primary"
            self.option4["style"] = "danger"
        elif answer==self.option4["text"]["text"]:
            self.option1["style"] = "danger"
            self.option2["style"] = "danger"
            self.option3["style"] = "danger"
            self.option4["style"] = "primary"

    


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
    

    """
    def _get_pin_block(self):
        task_checkmark = self._get_checkmark(self.pin_task_completed)
        text = (
            f"{task_checkmark} *Pin this message* :round_pushpin:\n"
            "Important messages and files can be pinned to the details pane in any channel or"
            " direct message, including group messages, for easy reference."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/205239997-Pinning-messages-and-files"
            "|Learn How to Pin a Message>*"
        )
        return self._get_task_block(text, information)


    def _get_reaction_block(self):
        task_checkmark = self._get_checkmark(self.reaction_task_completed)
        text = (
            f"{task_checkmark} *Add an emoji reaction to this message* :thinking_face:\n"
            "You can quickly respond to any message on Slack with an emoji reaction."
            "Reactions can be used for any purpose: voting, checking off to-do items, showing excitement."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions|"
            "Learn How to Use Emoji Reactions>*"
        )
        return self._get_task_block(text, information)


    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_check_mark:"
        return ":white_large_square:"

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]

    
    """