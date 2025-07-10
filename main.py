# main.py

import threading
from flask import Flask
from client import bot

# 🌐 Flask App Setup
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Bot is running!"

# ✅ Run Flask server in a separate thread
def run_flask():
    print("✅ Flask server started")
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    # Start Flask
    threading.Thread(target=run_flask).start()

    # ✅ Start bot with built-in idle and loop handling
    print("🤖 Starting bot...")
    bot.run()  # ✅ This is the correct method to run the bot
