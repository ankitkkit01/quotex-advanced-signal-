import logging
from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext
from utils.analysis import generate_signal, get_market_analysis
from utils.charts import generate_statistics_chart
from config import BOT_TOKEN, CHAT_ID
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("📊 Stats"), KeyboardButton("🎯 New Signal")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text(
        "👋 Welcome *Ankit Singh* to your *Professional Quotex Signal Bot*\n\n"
        "Use the buttons below to get started.",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def signal(update: Update, context: CallbackContext):
    pair, trend, confidence = generate_signal()
    analysis = get_market_analysis(pair)
    time_now = datetime.now().strftime("%I:%M %p")

    text = (
        f"📢 *Ankit AI Signal* ⚙️\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💹 *Pair:* `{pair}`\n"
        f"📈 *Direction:* {trend}\n"
        f"🕐 *Time:* {time_now}\n"
        f"📊 *Confidence:* {confidence}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📘 *Analysis:*\n"
        f"{analysis}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"Generated for: *Ankit Singh*"
    )
    update.message.reply_text(text, parse_mode='Markdown')

def stats(update: Update, context: CallbackContext):
    image_path, stats_text = generate_statistics_chart()

    with open(image_path, 'rb') as photo:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=stats_text, parse_mode='Markdown')

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("signal", signal))
    dp.add_handler(CommandHandler("stats", stats))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
