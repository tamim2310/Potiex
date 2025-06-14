import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from config import BOT_TOKEN, ADMIN_ID
from handlers import register_handlers
import os
from flask import Flask, request

# Initialize bot with state storage
bot = telebot.TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())

# Flask app for webhook
app = Flask(__name__)

# Define states for FSM
class UserState(StatesGroup):
    LANGUAGE = State()
    JOIN_VERIFICATION = State()
    BROKER_SELECTION = State()
    REGISTRATION = State()
    ACCOUNT_ID = State()
    QUOTE_TYPE = State()
    SIGNAL_TIME = State()
    CURRENCY_PAIR = State()
    SHOW_SIGNAL = State()

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return '', 403

def main():
    # Register all handlers
    register_handlers(bot)
    
    # Remove any existing webhook to avoid conflicts
    bot.remove_webhook()
    
    # Set webhook (Replace with your Render URL after deployment)
    webhook_url = f"https://{os.getenv('RENDER_APP_NAME', 'your-app-name')}.onrender.com/webhook"
    bot.set_webhook(url=webhook_url)
    
    # Get port from Render environment variable
    port = int(os.getenv("PORT", 5000))
    host = "0.0.0.0"
    
    print(f"Bot is running with webhook at {webhook_url} on port {port}...")
    
    # Start Flask server
    app.run(host=host, port=port)

if __name__ == "__main__":
    main()
