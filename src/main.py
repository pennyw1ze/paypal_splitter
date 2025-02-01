###################################################################
# IMPORT SECTION
from bot_functions import run_bot
###################################################################
# MAIN FUNCTION

if __name__ == '__main__':
    # Main function'
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nInterrupt received! Exiting...")
        print("Bot stopped.")

###################################################################
# END OF FILE