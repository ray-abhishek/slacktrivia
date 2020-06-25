# Quiz App for Slack 

Welcome to Quiz App for Slack! We wanted to make our Slack Channels more interactive and fun with an inhouse Quiz Bot. 
Through this, any Team Member can create a custom quiz/or fetch pre-existing questions category wise and release it in the channel for other members to attempt. We're hoping this leads to more interaction among Team Members.

We also hope that you enjoy playing around with this App just as much as we enjoyed building it.

Building For Slack 
------------------
Docs : https://api.slack.com/#read_the_docs

There are two main Slack APIs we'll be using to connect with Slack.
1. Events API ( https://api.slack.com/events-api )
    
    There are multiple type of events, and in order to trigger something on Slack based on an event, we'll need to use Events API to listen to those events. 

2. Web API ( https://api.slack.com/web )

    We're using Web API to push messages or update previously pushed messages. To push messages we're using chat.postMessage(). To update messages we're using chat.update(). 


-Example Scenario-

Suppose we have pushed a message to Slack using chat.postMessage() of WebAPI and we want the message to be updated with additional info every time an User reacts with an emoji to it. In that case, we can use Events API 'add_reaction' method to listen to such events, and then we can use chat.update() method of Web API, which takes a previously pushed message as a parameter and updates that specific message. 


What Slack Needs From Backend 
-----------------------------

Messages can be plain text or interactive. If we want to send interactive messages( in other words, messages that have buttons etc in them which Users can respond to ), we'll need to use Block Kits which is a UI Framework of Slack. 
Block Kits are in JSON Format.

Whatever messages we'll be sending to Slack through chat.postMessage() are basically a pre defined JSON format specific to UI that we want the message to have. 

Slack makes this process of building those JSON files much easier by having an interactive UI Building Interface called Block Kit Builder ( https://app.slack.com/block-kit-builder ) using which you can drag and drop UI elements and Slack will prepare the JSON format for you.

