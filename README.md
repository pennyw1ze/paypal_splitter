# paypal_splitter
Basic telegram bot to split paypal payments between friends.
The bot collects the subscription by the user, with the command add me.
When a user is added, his name is inserted into the database.
In the database, along with the user name, are stored also the amount of money owed for Netflix and for Spotify.
When a user wants to check if he owes money to the admin, he sends the command Check payments.
The commands shows the amount of money owed for Netflix and Spotify, and generates a personalized paypal link with the total amount of money owed by the user. It the user clicks on the link, he is redirected to paypal to perform the payment for the admin of the system.
The bot is able to detect the user payment trought the gmail apis. The bot is running a self hosted server, reachable on the web thanks to the interface provided by ngrok for free. When an email from paypal is received to the admin gmail account, the gmail webhooks redirect it to the bot. The bot checks if the email is sent from paypal, extract the amount and updates the user database. After this operations, sends a response to the user.
When a cyclic payment is received (month payment for Netflix or Spotify), the bot detects the payment, extract and split the amount, and updates the database of each user respectively subscribed to Spotify or Netflix.
All this mechanism can be run completely for free.

## Dependencies
Software required to run the bot script (all the bash code is for debian machines).
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
- Start;
- Check payments;
- Add me;
- Help;
