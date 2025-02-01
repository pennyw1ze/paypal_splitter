###################################################################
# IMPORT SECTION
from bot_functions import run_bot
from webhook_handler import start_server, start_ngrok
###################################################################
# MAIN FUNCTION

if __name__ == '__main__':
    # Main function'

    # Start ngrok service
    ngrok_process = start_ngrok()
    print(f"ngrok started with PID: {ngrok_process.pid}")
    
    # Start the server in a separate thread
    server_process = start_server()
    print(f"Server started with PID: {server_process.pid}")

    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nInterrupt received! Exiting...")
        # Forward the interrupt signal to the server process
        server_process.terminate()
        server_process.wait()
        print("Server process terminated.")
        ngrok_process.terminate()
        ngrok_process.wait()
        print("ngrok process terminated.")
        print("Bot stopped.")

###################################################################
# END OF FILE