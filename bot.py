import os
import random
import asyncio
import requests
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- 1. Flask Server (Keep-Alive for Render) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running perfectly!"

def run():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()

# --- 2. BOT & API SETTINGS ---
BOT_TOKEN = "8936154774:AAGyk5043s6YjZSjvesd9kmiAx-05T-TNhQ"
CHAT_ID = "@flashtrx7"

API_URL = "https://draw.ar-lottery01.com/TrxWinGo/TrxWinGo_1M/GetHistoryIssuePage.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) Chrome/139.0.0.0 Mobile Safari/537.36",
    "Referer": "https://hgnice.biz"
}

predictions_history = {}

def get_latest_game_data():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "list" in data["data"]:
                return data["data"]["list"]
    except Exception as e:
        print(f"API Fetch Error: {e}")
    return None

# --- 3. COMMAND HANDLERS ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 **TRX WinGo Auto Signal Bot အလုပ်လုပ်နေပါပြီ!**", parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ /start သို့မဟုတ် /signal ကို နှိပ်ပါ ခင်ဗျာ။", parse_mode="Markdown")

async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    history = get_latest_game_data()
    if history and len(history) > 0:
        latest_issue = str(history[0].get("issueNumber", "N/A"))
        next_issue = str(int(latest_issue) + 1) if latest_issue.isdigit() else "N/A"
        pred = random.choice(["BIG 🟢", "SMALL 🔴"])
        
        msg = (
            f"📊 **TRX 1-MIN VIP SIGNAL**\n"
            "-----------------------\n"
            f"🎲 **PERIOD:** `{next_issue}`\n"
            f"🎯 **PREDICTION:** **{pred}**\n"
            "-----------------------\n"
            "⚠️ *Invest Responsibly!*"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ Game API ထံမှ Data ရယူ၍ မရသေးပါ။ ခဏစောင့်ပါ။")

# --- 4. AUTO SIGNAL LOOP ---
async def auto_send_signals(application: Application):
    while True:
        try:
            history = get_latest_game_data()
            if history and len(history) > 0:
                latest_record = history[0]
                latest_period = str(latest_record.get("issueNumber"))
                winning_number = int(latest_record.get("number", 0))
                actual_result = "BIG 🟢" if winning_number >= 5 else "SMALL 🔴"

                if latest_period in predictions_history:
                    predicted_val = predictions_history[latest_period]
                    status_str = f"✅ **RESULT: WIN ({actual_result})** 🟢" if predicted_val == actual_result else f"❌ **RESULT: LOSE ({actual_result})** 🔴"
                    
                    result_msg = (
                        f"📊 **TRX 1-MIN RESULT**\n"
                        f"🎲 **PERIOD:** `{latest_period}`\n"
                        f"🔢 **NUMBER:** `{winning_number}`\n"
                        f"{status_str}"
                    )
                    await application.bot.send_message(chat_id=CHAT_ID, text=result_msg, parse_mode="Markdown")
                    del predictions_history[latest_period]

                next_period = str(int(latest_period) + 1)
                new_prediction = random.choice(["BIG 🟢", "SMALL 🔴"])
                predictions_history[next_period] = new_prediction

                signal_msg = (
                    f"📊 **TRX 1-MIN VIP SIGNAL**\n"
                    "-----------------------\n"
                    f"🎲 **PERIOD:** `{next_period}`\n"
                    f"🎯 **PREDICTION:** **{new_prediction}**\n"
                    "-----------------------\n"
                    "⚠️ *Invest Responsibly!*"
                )
                await application.bot.send_message(chat_id=CHAT_ID, text=signal_msg, parse_mode="Markdown")
            
        except Exception as e:
            print(f"Error in signal loop: {e}")

        await asyncio.sleep(60)

# --- 5. MAIN BOT RUNNER ---
async def post_init(application: Application):
    asyncio.create_task(auto_send_signals(application))

def main():
    keep_alive()

    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("signal", signal_command))

    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
