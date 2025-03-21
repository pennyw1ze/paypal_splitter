# paypal_splitter

## Project description
Basic telegram bot to **split paypal payments** between friends.
The bot collects the subscription by the user, with the command add me.

When a user is added, his name is inserted into the **database**.
In the database, along with the user name, are stored also the amount of money owed for **Netflix** and for **Spotify**.
When a user wants to check if he owes money to the admin, he sends the command Check payments.
The commands shows the amount of money owed for Netflix and Spotify, and generates a personalized paypal link with the total amount of money owed by the user. If the user clicks on the link, he is redirected to paypal to perform the payment for the admin of the system.

The bot is able to **detect the user payment** trought the gmail apis. The bot is running a **self hosted server**, reachable on the web thanks to the **interface** provided by **ngrok** for free. When an email from paypal is received to the admin gmail account, the gmail webhooks redirect it to the bot. The bot checks if the email is sent from paypal, extract the amount and updates the user database. After this operations, sends a response to the user.

When a **cyclic payment** is received (month payment for Netflix or Spotify), the bot **detects** the payment, extract and **split** the amount, and updates the database of each user respectively subscribed to Spotify or Netflix.

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
Run the command provided by ngrok to start the tunnel (just for testing, the bot will run the server holding the ngrok url):
```bash
ngrok http --url=<domain_name> 80
```
- Google authentication services:
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib --break-system-package
```

## Developer istructions
The admin that wants to run his own bot must follow this steps in order to configure the bot.
Remember that each file in the src folder MUST ONLY CONTAIN PRIVATE INFORMATION that you inserted following this steps, and **ALL THE PLACEHOLDER STRINGS MUST BE REPLACED**.
- Generate a paypalme link and copy-paste it to src/paypal_me_link_sample.txt;
- Generate a Telegram bot token and copy paste it to src/TOKEN_SAMPLE.txt (This is a guide that shows how to get the token. https://core.telegram.org/bots/tutorial#obtain-your-bot-token);
- Copy-paste the ngrok url in the form --url=something.like.this.ngrok-whatever;
- You must follow a guide in order to enable the gmail webhook service (wich is free). It is not complicate, but you must spend 20 minutes to enable the webhook from your account settings. This is an online guide: https://hevodata.com/learn/gmail-webhook/#step3, you will probably need to check other guides in order to achieve the goal. 

Whenever a link is asked to redirect emails to, provides the ngrok url. A secret.json file should be provided. Put the file inside the src folder.

Once you run the main function, it will asks you for the login with your google account in order to read and write emails. Grant permission, and a token.pickle file will be generated in your src folder.

After you are done with this steps, rename the files by removing the _sample tag, or just run the following command from the paypal_splitter folder:
```bash
mv ngrok_url_sample.txt ngrok_url.txt
mv TOKEN_SAMPLE.txt TOKEN.txt
mv paypal_me_link_sample.txt paypal_me_link.txt
```

- Customize the admin id and the list of person sharing the Neflix and Spotify account in the bot_function.py file by just inserting the name and the admin id;

### Attention!
All the message sent by the bot are in Italian lenguage.

Feel free to change the lenguage as you wish.

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
addme - Send request to be added to the bot
help - If you need help or the bot does not work
```
in order to create the following commands:
- Start;
- Check payments;
- Add me;
- Help;
