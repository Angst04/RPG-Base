# app.py

from threading import Thread
import main
import server

# Run the Telegram bot in a separate thread
bot_thread = Thread(target=main.bot.polling, args=(), kwargs={"none_stop": True})
bot_thread.start()

# Run the Flask server
if __name__ == '__main__':
   server.app.run()