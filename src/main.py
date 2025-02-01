###################################################################
# IMPORT SECTION
from bot_functions import run_bot
from webhook_handler import start_server, start_ngrok
import threading
import signal
import sys
###################################################################
# MAIN FUNCTION

if __name__ == '__main__':
    # Main function'

    # Function to handle interrupt signal
    def signal_handler(_sig, _frame):
        print("\nInterrupt received! Exiting...")
        if server_thread.is_alive():
            server_thread.join()
            print("Server thread terminated.")
        if ngrok_thread.is_alive():
            ngrok_thread.join()
            print("ngrok thread terminated.")
        print("Bot stopped.")
        sys.exit(0)

    try:
        # Start ngrok service in a separate thread
        ngrok_thread = threading.Thread(target=start_ngrok)
        ngrok_thread.start()
        print("ngrok thread started.")

        # Start the server in a separate thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()
        print("Server thread started.")

        # Register the signal handler
        signal.signal(signal.SIGINT, signal_handler)

        # Run the bot in the main thread
        run_bot()
    except KeyboardInterrupt:
        signal_handler(None, None)

###################################################################
# END OF FILE