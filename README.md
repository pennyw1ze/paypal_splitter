# paypal_splitter
Basic telegram bot to split paypal payments between friends.

## Requirements
- python3:
```bash
sudo apt install python3
```
- pip:
```bash
sudo apt install python3-pip
```
- python-telegram-bot:
```bash
pip install python-telegram-bot
```
In case of "error: externally-managed-environment", run:
```bash
pip install python-telegram-bot --break-system-packages
```
to force the installation.
- ngrok:
```bash
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| sudo tee /etc/apt/sources.list.d/ngrok.list \
	&& sudo apt update \
	&& sudo apt install ngrok
```
Then create an account on [ngrok](https://ngrok.com/) and run:
```bash
ngrok config add-authtoken <your_auth_token>
```
Select the Static domain, generate it for free.
Run the command provided by ngrok to start the tunnel:
```bash
ngrok http --url=<domain_name> 80
```
- Google authentication services:
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib --break-system-package
```
## Bot setup via @BotFather
I set up a list of commands, a profile picture and a short description via BotFather.
Just follow the steps:
- Open "menu";
- Select "edit your bots";
- Select your bot;
- Tap on "Edit Bot";
- Now, select "Edit Commands";
- Here, send to the bot the following string:
```
start - How to use the bot
payments - Verify payments
help - If you need help or the bot does not work
```
  in order to create the following commands:
  > Start;
  > Check payments;
  > Help;
