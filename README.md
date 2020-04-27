# Track My Slack

Track My Slack is a slack bot that alerts workspace members when they mention a key phrase. Users have the ability to add or delete trackable phrases. 

![image](https://user-images.githubusercontent.com/5722230/80339092-c1c62a80-8812-11ea-8bbf-30b8309f8d15.png)

## Setup

### Before we can run `docker-compose up`, we'll need to take care of a few things related to the way Slack grants permissions and routes requests. 

#### Setup ngrok, a tunnelling software 

1. Navigate to https://ngrok.com/ and download ngrok for your operating system (this is required because Slack uses request URLs)
2. Open up a terminal window
3. Unzip ngrok: `unzip /path/to/ngrok.zip`
4. Run the following command: `./ngrok authtoken <AUTH_TOKEN>` -- replace auth token with the auth token listed on step two of this page: https://dashboard.ngrok.com/get-started/setup
5. Run `./ngrok http 5000` -- you should see the following: 
![image](https://user-images.githubusercontent.com/5722230/80339148-defaf900-8812-11ea-8ade-bea700c8c455.png)
6. Save the second "Forwarding" URL for later. It will look like this: `https://<some-string>.ngrok.io`
  
#### Configure slash commands
1. Login to a Slack workspace of your choosing through the browser, where you'll be creating an app to test the bot
2. Navigate to https://api.slack.com/
3. Click 'Your Apps' in the top right corner
4. Create an app
5. Click 'Basic Information' within the 'Settings' menu, and scroll to 'Add Credentials' -- next to 'Signing Secret' click 'Show' -- copy and save for later
5. Click "Slash Commands" within the "Features" menu -- this is where we'll configure our commands for adding and deleting phrases to the watch-list
6. Click 'Create New Command'
7. Fill it out like so:
![image](https://user-images.githubusercontent.com/5722230/80339179-efab6f00-8812-11ea-85f0-8cc87a3e6964.png)
8. For the 'Request URL' field, copy and paste the ngrok url from step (6), and add `/add_phrase` to the end of it 
8. Save changes!
9. Duplicate steps 6 - 8 for 'delete_phrase'

Congrats! You've configured the slash commands to add and remove watch phrases. 

#### Configure permissions
1. Navigate to "OAuth & Permissions" in the "Features" menu
2. Click 'Install App to Workspace'
3. Click 'Allow'
4. Copy the 'Bot User OAuth Access Token' for later
5. Scroll down to 'Scopes'
6. Under 'Bot Token Scopes', click 'Add an OAuth Scope'
7. Add the following additional bot scopes: im:write, channels:history
8. Re-install your app:
![image](https://user-images.githubusercontent.com/5722230/80339123-d276a080-8812-11ea-9e78-d30dd2fdd5af.png)

#### Setup Environment Variables

1. Open up a terminal window
2. Clone the respository into a directory of your choice: `git clone https://github.com/codybreene/slack_bot.git`
3. `cd` into the `slack_bot` directory
3. Create a file in that directory to store your environment variables: `touch .env`
4. Open up the directory in a coding editor of your chosing, and navigate to the `.env` file
5. Add the following:
```
SLACK_SIGNING_SECRET=<SIGNING_SECRET>
SLACK_BOT_TOKEN=<BOT_TOKEN>
AIRTABLE_BASE_KEY=appvq9i1bO2gEbi6Y
AIRTABLE_API_KEY=key54bic9Lngk71On
```
6. Replace <SIGNING_SECRET> with the signing secret you copied from 'Basic Information' (three sections up, step 5)
7. Replace <BOT_TOKEN> with the Bot User OAuth Access Token you copied (two sections up, step 4)
8. Save the file

#### Launch the app
1. Ensure you have Docker installed: https://docs.docker.com/get-docker/
2. Ensure you're not running any docker containers: `docker ps` then `docker stop <CONTAINER_ID>`
3. Run: `docker-compose up`
4. Navigate to `localhost:5000`, and you should see an indication the app is running

#### Add Event Subscriptions 
1. Navigate back to your app dashboard on the Slack website
2. Click on 'Event Subscriptions' in the 'Features' menu
3. Toggle events on
4. Copy the ngrok URL from the previous section, paste it into the 'Request URL' field and add `/events`:
![image](https://user-images.githubusercontent.com/5722230/80340059-c7bd0b00-8814-11ea-8cc9-ae195475cb49.png)
5. Click 'Subscribe to bot events'
6. Click 'Add Bot User Event' and add the `message.channels` event:
![image](https://user-images.githubusercontent.com/5722230/80340054-c390ed80-8814-11ea-92a6-97e09613a80a.png)
7. Save changes!

#### Test it out!
1. Open up the slack workspace
2. Type some test messages
3. Type some slash commands `/add_phrase` and `/delete_phrase`

## Technologies
* Flask
* Docker
* Slack Events API
* Airtable API
* ngrok 
