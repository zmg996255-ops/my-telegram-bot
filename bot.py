import asyncio
import random
from telegram import Bot
from telegram.error import TelegramError

# --- သင့် BOT TOKEN နဲ့ CHANNEL ID ---
BOT_TOKEN = "8962054022:AAFfTE43NRJKa7Wv8IYq9xvz29roLUZ"
CHAT_ID = "@flashtrx77"


def generate_signal():
    period = random.randint(20260001, 20269999)
    prediction = random.choice(["BIG 🟢", "SMALL 🔴"])
    pattern = random.choice(["1 MINUTE WINGO", "TRX VIP SIGNAL"])

    return (
        f"📊 **{pattern}**\n"
        "----------------------------\n"
        f"🎲 **PERIOD:** `{period}`\n"
        f"🎯 **PREDICTION:** **{prediction}**\n"
        "----------------------------\n"
        "⚠️ *Invest Responsibly!*"
    )


async def send_signal():
    bot = Bot(token=BOT_TOKEN)
    message = generate_signal()
    try:
        await bot.send_message(
            chat_id=CHAT_ID, text=message, parse_mode="Markdown"
        )
        print("Signal Sent!")
    except TelegramError as e:
        print(f"Error: {e}")


async def main():
    print("Bot online...")
    while True:
        await send_signal()
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
