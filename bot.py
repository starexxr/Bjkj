import subprocess
import threading
import time
import requests
import urllib.parse
from flask import Flask, request, jsonify
import os
import telebot
from telebot.types import Message
from utils.conf import *

app = Flask(__name__)

bot = telebot.TeleBot(API_TOKEN)
process = None
monitor_thread = None
monitor_stop = threading.Event()

@app.route('/')
def home():
    if process is not None and process.poll() is None:
        return jsonify({"status": 1})
    else:
        return jsonify({"status": 0})

@app.route('/health')
def health():
    return "OK"

@app.route('/f')
def add_friend_web():
    uid = request.args.get('uid')
    if not uid:
        return jsonify({"error": "UID parameter is required"}), 400
    
    api_url = ADD_FRIEND_API.replace("{uid}", uid)
    try:
        response = requests.get(api_url, timeout=10)
        return jsonify({"status": response.status_code, "message": "Friend request processed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/b')
def change_bio_web():
    bio = request.args.get('bio')
    if not bio:
        return jsonify({"error": "Bio parameter is required"}), 400
    
    encoded_bio = urllib.parse.quote(bio)
    api_url = CHANGE_BIO_API.replace("{bio}", encoded_bio)
    try:
        response = requests.get(api_url, timeout=10)
        return jsonify({"status": response.status_code, "message": "Bio update processed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/on')
def start_bot_web():
    global process, monitor_thread, monitor_stop
    if process is None:
        try:
            process = subprocess.Popen(["python", BOT_FILE])
            monitor_stop.clear()
            monitor_thread = threading.Thread(target=monitor_process, args=("web",), daemon=True)
            monitor_thread.start()
            return jsonify({"status": "success", "message": "Bot started"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"status": "already_running", "message": "Bot is already running"})

@app.route('/off')
def stop_bot_web():
    global process, monitor_stop
    if process:
        try:
            process.terminate()
            process.wait(timeout=5)
            process = None
            monitor_stop.set()
            return jsonify({"status": "success", "message": "Bot stopped"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"status": "not_running", "message": "Bot is not running"})

def monitor_process(chat_id):
    global process
    while not monitor_stop.is_set():
        if process:
            ret = process.poll()
            if ret is not None:
                time.sleep(5)
                restart_bot(chat_id)
        time.sleep(2)

def restart_bot(chat_id):
    global process
    try:
        process = subprocess.Popen(["python", BOT_FILE])
        if chat_id != "web":
            bot.send_message(chat_id, "Bot restarted.")
    except Exception as e:
        if chat_id != "web":
            bot.send_message(chat_id, f"Restart error: {e}")

@bot.message_handler(commands=['run'])
def run_bot_handler(message: Message):
    global process, monitor_thread, monitor_stop
    
    if process is None:
        try:
            process = subprocess.Popen(["python", BOT_FILE])
            monitor_stop.clear()
            monitor_thread = threading.Thread(target=monitor_process, args=(message.chat.id,), daemon=True)
            monitor_thread.start()
            bot.reply_to(message, "Bot Started.")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
    else:
        bot.reply_to(message, "Bot is already running.")

@bot.message_handler(commands=['stop'])
def stop_bot_handler(message: Message):
    global process, monitor_stop
    
    if process:
        try:
            process.terminate()
            process.wait(timeout=5)
            process = None
            monitor_stop.set()
            bot.reply_to(message, "Bot stopped.")
        except Exception as e:
            bot.reply_to(message, f"Stop error: {e}")
    else:
        bot.reply_to(message, "Bot is not running.")

@bot.message_handler(commands=['status'])
def status_handler(message: Message):
    if process and process.poll() is None:
        bot.reply_to(message, "Bot is running.")
    else:
        bot.reply_to(message, "Bot is not running.")

@bot.message_handler(commands=['friend'])
def add_friend_handler(message: Message):
    text_parts = message.text.split()
    
    if len(text_parts) < 2:
        bot.reply_to(message, "Please provide UID. Usage: /friend 123456789")
        return
    
    uid = text_parts[1]
    api_url = ADD_FRIEND_API.replace("{uid}", uid)
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            bot.reply_to(message, f"Friend request sent to UID: {uid}")
        else:
            bot.reply_to(message, f"API responded with status: {response.status_code}")
    except requests.exceptions.Timeout:
        bot.reply_to(message, "Request timed out.")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['bio'])
def change_bio_handler(message: Message):
    text_parts = message.text.split(maxsplit=1)
    
    if len(text_parts) < 2:
        bot.reply_to(message, "Please provide bio text. Usage: /bio Your new bio text")
        return
    
    bio_text = text_parts[1]
    encoded_bio = urllib.parse.quote(bio_text)
    api_url = CHANGE_BIO_API.replace("{bio}", encoded_bio)
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            bot.reply_to(message, "Bio changed.")
        else:
            bot.reply_to(message, f"API responded with status: {response.status_code}")
    except requests.exceptions.Timeout:
        bot.reply_to(message, "Request timed out.")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

def start_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def main():
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    print("Controller Initialised")
    bot.infinity_polling()

if __name__ == "__main__":
    main()
