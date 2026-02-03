from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.fastapi import SlackRequestHandler
from fastapi import FastAPI ,Request
import os
import requests 
import json
from views.views_all import add_project_view

import logging
from db.init_db import init_db

init_db()

# Right now inti_db() is called here but in future it should be called from alembic migration scripts
# Reason is that alembic will handle all the database versioning and migration logic
# schema changes are done by migrations and app assumes that database already exists 
# Hence init_db() will be removed in production code 


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

from routers import deprecated_welcome_route, resume_route
load_dotenv()
bot_token=os.environ['SLACK_BOT_TOKEN']
sign_secret=os.environ['SLACK_SIGNING_SECRET']
# app_token=os.environ['SLACK_APP_TOKEN']
FASTAPI_URL=os.environ['FASTAPI_URL']
FASTAPI_URL2=os.environ['FASTAPI_URL2']
FASTAPI_URL3=os.environ['FASTAPI_URL3']



slack_app=App(token=bot_token,signing_secret=sign_secret)
#app.client.chat_postMessage(channel="C0A92BHGUDV",text="Hello")
server=FastAPI(title="Project Matcher App")

server.include_router(router=deprecated_welcome_route.router)
server.include_router(router=resume_route.router,prefix='/resume')

@slack_app.event("message")
def log_event(event,say,client):
    usr_message=event['text']
    channel_id=event['channel']
    thread_ts=event['event_ts']
    print(usr_message)
    say(channel=channel_id,text=usr_message,thread_ts=thread_ts)
    client.chat_postMessage(channel="C0A92BHGUDV",text="I just replied to you check out")

@slack_app.command("/repeat-me")
def open_project_form(ack,body,logger,client):
    ack("Your command request is received , Thank You slack")
    logger.info(f'This command was sent by {body['user_id']}')
    my_text= f'You are saying: {body['text']}'
    client.chat_postMessage(channel=body['channel_id'],text=my_text)



@slack_app.command("/add-project")
def open_project_form(ack, body, client,logger):
    ack()

    # This body is the interaction payload 
    # using command is interaction and interaction payload is sent at webhook URL
    # this interaction payload has trigger id attribute , which must be used within 3 seconds after that it expires
    # we pass trigger id and views object (how form should look) to client.views_open()
    # that popup form is called modal and client.view_open() exactly opens that for user 
    # so that user can type in the reponse 

    #When your app receives an interaction payload from Slack, that payload includes a trigger_id
    #The trigger ID in Slack is a temporary, single-use identifier generated when a user interacts with your app
    #The client.views_open() method in the Slack API uses a trigger_id to open a modal (a pop-up window) on the user's screen. 
    # in callback_id we name the view 

    trigger_id = body["trigger_id"]

    client.views_open(
        trigger_id=trigger_id,
        view=add_project_view
        # view={
        #     "type": "modal",
        #     "callback_id": "project_form",
        #     "title": {"type": "plain_text", "text": "Add Project"},
        #     "submit": {"type": "plain_text", "text": "Save"},
        #     "close": {"type": "plain_text", "text": "Cancel"},
        #     "blocks": [
        #         {
        #             "type": "input",
        #             "block_id": "title_block",
        #             "label": {"type": "plain_text", "text": "Project Title"},
        #             "element": {
        #                 "type": "plain_text_input",
        #                 "action_id": "title"
        #             }
        #         },
        #         {
        #             "type": "input",
        #             "block_id": "desc_block",
        #             "label": {"type": "plain_text", "text": "Description"},
        #             "element": {
        #                 "type": "plain_text_input",
        #                 "multiline": True,
        #                 "action_id": "description"
        #             }
        #         },
        #         {
        #             "type": "input",
        #             "block_id": "tech_block",
        #             "label": {"type": "plain_text", "text": "Tech Stack"},
        #             "element": {
        #                 "type": "plain_text_input",
        #                 "action_id": "tech"
        #             }
        #         }
        #     ]
        # }
    )

    logger.info("Checkpoint 1: Modal displayed")


@slack_app.view("project_form")
def handle_project_submission(ack, body, view,logger):
    ack()

    # view object has lot of attributes , one is state attribute , state attibute has value attribute
    # then value attribute has blocks attribute which further has field name attribute which finally has a value attribute 
    
    # body object here is again the interaction payload 
    # that interaction payload will have information about the user , which user interacted with it 
    
    print(body)
    print("VIEW")
    print(view)
    values = view["state"]["values"]


    title = values["title_block"]["title"]["value"]
    description = values["desc_block"]["description"]["value"]
    # some data preprocessing of split(",") is done here also 
    tech_stack = values["tech_block"]["tech"]["value"].split(",")
    logger.info(f"PROJECT: {title} , {description},{tech_stack}")
    payload = {
        "title": title,
        "description": description,
        "tech_stack": tech_stack,
        "created_by": body["user"]["id"]
    }
    # here json=payload automatically calls json.dumps(payload)
    response = requests.post(FASTAPI_URL, json=payload)
    print(response.json())

############################################################
#############################################################
###############################################################
##############################################################

@slack_app.command("/find-project")
def open_job_form(ack, body, client,logger):
    ack()
    trigger_id = body["trigger_id"]
    client.views_open(
        trigger_id=trigger_id,
        # Can not put this view in separate file because of its dependency on body variable
        view={
            "type": "modal",
            "callback_id": "job_form",
            "private_metadata": body["channel_id"], # we have passed channel id here so that we can use it later to post message
            "title": {"type": "plain_text", "text": "Add Job Description"},
            "submit": {"type": "plain_text", "text": "Save"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "job_block",
                    "label": {"type": "plain_text", "text": " Job Description"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "job_description",
                        "multiline": True,
                    }
                },
            ]
        }
    )

    logger.info("Checkpoint 2: Modal 2 displayed")


@slack_app.view("job_form")
def handle_job_submission(ack, body, view,logger,client):
    ack()

    # view object has lot of attributes , one is state attribute , state attibute has value attribute
    # then value attribute has blocks attribute which further has field name attribute which finally has a value attribute 
    
    # body object here is again the interaction payload 
    # that interaction payload will have information about the user , which user interacted with it 
    
    print(body)
    print("VIEW")
    print(view)
    values = view["state"]["values"]


    job = values["job_block"]["job_description"]["value"]
    payload = {
        "job_description": job,
        "created_by": body["user"]["id"]
    }
    # here json=payload automatically calls json.dumps(payload)
    response = requests.post(FASTAPI_URL2, json=payload)
    print(type(response))
    print(type(response.json()))
    logger.info(f"Response: {response.json()}")
    print(response.json())
    client.chat_postMessage(channel=view['private_metadata'],text=json.dumps(response.json(), indent=2))
    
############################################################
#############################################################
###############################################################
##############################################################

@slack_app.command("/add-job")
def save_job_form(ack, body, client,logger):
    ack()
    trigger_id = body["trigger_id"]
    client.views_open(
        trigger_id=trigger_id,
        # Can not put this view in separate file because of its dependency on body variable
        view={
            "type": "modal",
            "callback_id": "add_job_form",
            "title": {"type": "plain_text", "text": "Add Job Description"},
            "submit": {"type": "plain_text", "text": "Save"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "job_block",
                    "label": {"type": "plain_text", "text": " Job Description"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "job_description",
                        "multiline": True,
                    }
                },
            ]
        }
    )

    logger.info("Checkpoint 2: Modal 2 displayed")


@slack_app.view("add_job_form")
def save_job(ack, body, view,logger,client):
    ack()
    values = view["state"]["values"]
    job = values["job_block"]["job_description"]["value"]
    payload = {
        "job_description": job,
        "created_by": body["user"]["id"]
    }
    # here json=payload automatically calls json.dumps(payload)
    response = requests.post(FASTAPI_URL3, json=payload)
    logger.info(f"Response: {response.json()}")



# Slack handler
handler = SlackRequestHandler(slack_app)

# Slack event route

# So this adapter basically send the request to slack bolt framework and it handles the request on its own 
@server.post("/slack/events")
async def slack_events(req: Request):
    return await handler.handle(req)


# if __name__ == '__main__':
#     handler = SocketModeHandler(app=app,app_token=app_token)
#     handler.start()

# using ngrok and also flask you will make things 