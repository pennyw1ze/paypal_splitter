###################################################################
# IMPORT LIBRARIES
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# Import database functions
from db_functions import *
###################################################################
# GLOBAL VARIABLES

# Users lists
Ripetizioni = ["@brunette105"]
Netflix = ["@danidarge","@skhuuuu","@grev8"]
Spotify = ["@danidarge","@skhuuuu"]

# Admin ID
Admin = 351523902

# Users to ID dicrtionary
translate = {
    351523902: "@Leon4rd002",
    0: "@brunette105",
    1: "@danidarge",
    2: "@skhuuuu",
    3: "@grev8"
}

###################################################################
# GENERAL PURPOSE FUNCTIONS

# Get token from local folder
# File must be named "TOKEN.txt"
def get_token():
    with open("../data/TOKEN.txt", "r") as file:
        return file.read().strip()
    
# Get pretty formatted lists from database outcomes
def format(data):
    formatted = ""
    for user in data:
        formatted += f"{translate[user[0]]}:\n- Netflix: {user[1]}€;\n- Spotify: {user[2]}€;\n- Ripetizioni: {user[3]}€\n-----------------------\n"
    return formatted

###################################################################
# BOT FUNCTIONS

# Define hello command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Ciao {update.effective_user.first_name}, sono un bot creato per aiutare Leonardo a gestire i pagamenti.')

# Define help command handler
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Lorem ipsum dolor sit amet.\nIn caso di problemi contattare @Leon4rd002')

# Define pagamenti command handler
async def pagamenti(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the user is the admin
    if update.effective_user.id == Admin:
        await update.message.reply_text(format(get_all_users()))
    else:
        id = update.effective_user.id
        user = get_user(id)
        message = "Ciao {translate[id]}!\n"
        if user[1] + user[2] + user[3] == 0:
            await update.message.reply_text(message + "Non devi pagare niente, sei a posto!\n")
        else:
            if 
###################################################################
# MAIN FUNCTION

# Define main function
def main(cursor) -> None:
    # Debug message
    print("Bot started")
    
    # Create application
    app = ApplicationBuilder().token(get_token()).build()

    # Handle start command
    app.add_handler(CommandHandler("start", start))

    # Handle help command
    app.add_handler(CommandHandler("aiuto", help))

    # Handle pagamenti command
    app.add_handler(CommandHandler("pagamenti", pagamenti))

    # Run polling
    app.run_polling()

###################################################################
# MAIN FUNCTION

if __name__ == '__main__':
    # Function to build a local database that returns a cursor to navigate it
    cursor = build_database()
    # Add the admin
    add_user(Admin)
    # Main function
    main(cursor)

###################################################################
# END OF FILE