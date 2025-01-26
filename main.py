###################################################################
# IMPORT LIBRARIES
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
###################################################################
# GLOBAL VARIABLES

# Users lists
Ripetizioni = ["@brunette105"]
Netflix = ["@danidarge","@skhuuuu","@grev8"]
Spotify = ["@danidarge","@skhuuuu"]

# Admin ID
Admin = 351523902

###################################################################
# GENERAL PURPOSE FUNCTIONS

# Get token from local folder
# File must be named "TOKEN.txt"
def get_token():
    with open("TOKEN.txt", "r") as file:
        return file.read().strip()

###################################################################
# BOT FUNCTIONS

# Define hello command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Ciao {update.effective_user.first_name}, sono un bot creato per aiutare Leonardo a gestire i pagamenti.')

# Define help command handler
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Lorem ipsum dolor sit amet.\nIn caso di problemi contattare @Leon4rd002')

###################################################################
# MAIN FUNCTION

# Define main function
def main() -> None:
    # Debug message
    print("Bot started")
    
    # Create application
    app = ApplicationBuilder().token(get_token()).build()

    # Handle start command
    app.add_handler(CommandHandler("start", start))

    # Handle help command
    app.add_handler(CommandHandler("aiuto", help))

    # Handle pagamenti command
    app.add_handler(CommandHandler("pagamenti", help))

    # Run polling
    app.run_polling()

###################################################################
# MAIN FUNCTION

if __name__ == '__main__':
    main()

###################################################################
# END OF FILE