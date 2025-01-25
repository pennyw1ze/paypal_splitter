# paypal_splitter
Basic telegram bot to split paypal payments between friends.

## Requirements
- python3;
```bash
sudo apt install python3
```
- pip;
```bash
sudo apt install python3-pip
```
- python-telegram-bot;
```bash
pip install python-telegram-bot
```
In case of "error: externally-managed-environment", run:
```bash
pip install python-telegram-bot --break-system-packages
```
to force the installation.

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
