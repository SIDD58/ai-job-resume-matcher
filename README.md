
Install uv on your system 

How to use on Local

uv run uvicorn main:server --reload

here the main is file name and server is the fast api object we created 

then use ngrok http 8000

becasue 8000 is port where our local host is running 

it will give you something like this 
https://nonaromatic-heriberto-multipolar.ngrok-free.dev

go to api.slack.com 
in your event subscription , request URL , you have to put this 
in your slash command , request URL , you have to put this 
in interactivity and shortcuts , request URL , you have to put this 
Slack interactivity enables apps to respond to user actions


also in your .env file 
FASTAPI_URL=https://nonaromatic-heriberto-multipolar.ngrok-free.dev/resume/add-project
you have to change that here also 

Login to your slack is through workspace and not email : workspace
However you can login to slack using email also then you have to select workspace  
(Specific workspace , or go to slack.com/signin)

# How to run the code locally and setup you have to do 

# Make Flow Chart of how DATA Flows 

# What are the API Endpoints 

# How to use it from the slack 

# For testing also you need commands 

# System desing PAtterns Explanations 

# Data mapper patern , Dependecy injection and Factory Pattern 
# Low coupling between compoenents and best architecture followed  
