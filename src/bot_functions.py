###################################################################
# IMPORT LIBRARIES
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
# Import database functions
from db_functions import *
import os
import requests
###################################################################
# Mount the database
build_database()
###################################################################
# GLOBAL VARIABLES

# Admin ID
Admin = 351523902

# Base path
base_path = os.path.dirname(os.path.abspath(__file__))

# Translate dictionary
translate = {key: value for key, value in get_all_translate()}

# Netflix member list
Netflix = ["Leonardo"]

# Spotify member list
Spotify = ["Leonardo","Chiara"]

###################################################################
# GENERAL PURPOSE FUNCTIONS

# Get token from local folder
# File must be named "TOKEN.txt"
def get_token():
    token_path = os.path.join(base_path, '..', 'data', 'TOKEN.txt')
    with open(token_path, "r") as file:
        return file.read().strip()
    
# Get pretty formatted lists from database outcomes
def format(data):
    # Check if the list is empty
    if len(data) == 0:
        return "Non ci sono utenti registrati."
    # Format the list
    formatted = ""
    for user in data:
        formatted += f"{translate[user[0]]}:\n- Netflix: {user[1]}€;\n- Spotify: {user[2]}€;\n- Ripetizioni: {user[3]}€\n-----------------------\n"
    return formatted

# Get PayPal link from local folder
def get_paypal_link():
    paypal_link_path = os.path.join(base_path, '..', 'data', 'paypal_me_link.txt')
    with open(paypal_link_path, "r") as file:
        return file.read().strip()

# Process payment
def received_payment(name, amount):
    # Check if the user is in the database
    id = get_id(name)
    if id is None:
        send_telegram_message(f"L'utente {name} non è registrato (ricevuto pagamento di {amount}€).", Admin)
        return None
    # Process payment
    process_payment(id, amount)

    # Send confirmation message
    send_telegram_message(f"Ricevuto pagamento di {amount}€.", id)

    # Send confirmation message to the admin
    send_telegram_message(f"Ricevuto pagamento di {amount}€ da {name}.", Admin)

# Add Neflix mensility
def add_netflix(amount):
    single_rate = amount / len(Netflix)
    for member in Netflix:
        id = get_id(member)
        add_netflix_amount(id, single_rate)
        send_telegram_message(f"Aggiornamento rata di Netlix, aggiunti {single_rate}€.", id)

# Add Spotify mensility
def add_spotify(amount):
    single_rate = amount / len(Spotify)
    for member in Spotify:
        id = get_id(member)
        add_spotify_amount(id, single_rate)
        send_telegram_message(f"Aggiornamento rata di Spotify, aggiunti {single_rate}€.", id)

###################################################################
# BOT FUNCTIONS

# Send arbitrary message
def send_telegram_message(message, chat_id):
    telegram_url = f"https://api.telegram.org/bot{get_token()}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(telegram_url, json=payload)
    return response.json()

# Define hello command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Ciao {update.effective_user.first_name}, sono un bot creato per aiutare Leonardo a gestire i pagamenti.')

# Define help command handler
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Lorem ipsum dolor sit amet.\nIn caso di problemi contattare @Leon4rd002')

# Define add user command handler
async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Save user id
    id = update.effective_user.id
    # Check if the user is already registered
    if check_user_table(id) is not None:
        await update.message.reply_text(f"Sembra che tu sia già registrato!")
        return None
    # Add user to database
    add_user_table(id)
    add_translate(id, update.effective_user.first_name)
    # Update translate dictionary
    global translate
    translate = {key: value for key, value in get_all_translate()}
    await update.message.reply_text(f"Sei stato aggiunto con successo!")

# Define pagamenti command handler
async def pagamenti(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the user is in the database
    if check_user_table(update.effective_user.id) is None:
        await update.message.reply_text("Non sei registrato! Usa il comando /aggiungimi per registrarti.")
        return None
    # Check if the user is the admin
    if update.effective_user.id == Admin:
        await update.message.reply_text(format(get_all_users()))
        return None
    # Get user data
    id = update.effective_user.id
    user = get_user(id)
    message = f"Ciao {translate[id]}!\n"
    n,s,r = user[1],user[2],user[3]
    # Check if the user has to pay
    if user[1] + user[2] + user[3] == 0:
        await update.message.reply_text(message + "Non devi pagare niente, sei a posto!\n")
        return None
    # Create message
    message += "Ti rimangono da pagare:\n"
    if user[1] > 0:
        message += f"> {n}€ per Netflix.\n"
    if user[2] > 0:
        message += f"> {s}€ per Spotify.\n"
    if user[3] > 0:
        message += f"> {r}€ per le ripetizioni.\n"
    # Sends a message with three inline buttons attached
    keyboard = [
        [button for button in [
            InlineKeyboardButton(f"Salda Netflix ({n}€)", callback_data=f"{n}") if n > 0 else None,
            InlineKeyboardButton(f"Salda Spotify ({s}€)", callback_data=f"{s}") if s > 0 else None,
            InlineKeyboardButton(f"Salda Ripetizioni ({r}€)", callback_data=f"{r}") if r > 0 else None,
        ] if button is not None]
    ]
    if n*s > 0:
        keyboard.append([InlineKeyboardButton(f"Salda tutto ({n+s})€", callback_data=f"{n+s}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup)

# Define add amount command handler
async def add_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get user id
    id = update.effective_user.id
    # Check if the user is the admin
    if id != Admin:
        await update.message.reply_text("Non sei autorizzato ad eseguire questa operazione.")
        return None
    # Check if the command is formatted correctly
    if len(context.args) != 3:
        await update.message.reply_text("Il comando non è stato formattato correttamente.")
        return None
    # Message formatting: /aumenta <name> <service> <amount>
    name = context.args[0]
    service = context.args[1]
    amount = float(context.args[2])
    # Check if the user is in the database
    user = get_id(name)
    if user is None:
        await update.message.reply_text("L'utente non è registrato.")
        return None
    # Check if the service is valid
    if service not in ["Netflix", "Spotify", "Ripetizioni"]:
        await update.message.reply_text("Il servizio non è valido.")
        return None
    # Get payment data from user
    user = get_user(user)
    print(user)
    # Update the database
    if service == "Netflix":
        add_netflix_amount(user[0], amount + float(user[1]))
    elif service == "Spotify":
        add_spotify_amount(user[0], amount + float(user[2]))
    elif service == "Ripetizioni":
        add_ripetizioni_amount(user[0], amount + float(user[3]))
    # Send confirmation message
    await update.message.reply_text(f"Aggiornamento completato.")

# Define callback query handler
# CallbackQueries need to be answered, even if no notification to the user is needed
# Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    # Get user data
    id = update.effective_user.id
    user = get_user(id)
    # Get the service
    amount = round(float(query.data))
    # Check if the user has to pay
    if user[1] + user[2] + user[3] == 0:
        await query.edit_message_text("Non devi pagare niente, sei a posto!")
        return None
    # Send confirmation message
    link = get_paypal_link() + f"{amount}"
    await query.edit_message_text(text = f"Puoi procedere al pagamento di {amount}€ tramite PayPal al seguente link:\n{link}\nUna volta\
 completato il trasferimento, verrà aggiornato il tuo saldo. L'operazione potrebbe richiedere qualche minuto.")


###################################################################
# MAIN FUNCTION

# Define main function
def run_bot() -> None:
    # Debug message
    print(translate)
    # Debug message
    print("Bot started")
    
    # Create application
    app = ApplicationBuilder().token(get_token()).build()

    # Handle start command
    app.add_handler(CommandHandler("inizia", start))

    # Handle help command
    app.add_handler(CommandHandler("aiuto", help))

    # Handle pagamenti command
    app.add_handler(CommandHandler("pagamenti", pagamenti))

    # Handle add me" command
    app.add_handler(CommandHandler("aggiungimi", add_user))

    # ADMIN COMMANDS
    # Handle Increasing and decreasing amounts
    app.add_handler(CommandHandler("aumenta", add_amount))

    # Handle button press
    app.add_handler(CallbackQueryHandler(button))

    # Run polling
    app.run_polling()