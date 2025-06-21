import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from utils.analysis import generate_signal
from utils.charts import generate_statistics_chart
from config import BOT_TOKEN, CHAT_ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "📊 Welcome to Quotex Advanced Signal Bot\n"
        "🔥 Type /signal to get a new signal.\n"
        "📈 Type /stats to view performance.\n"
        "👤 Personalized for: *Ankit Singh*"
    )

def signal(update: Update, context: CallbackContext):
    update.message.reply_text("Please wait... Generating your personalized signal ⚙️")
    result = generate_signal()
    update.message.reply_text(result)

def stats(update: Update, context: CallbackContext):
    chart_path = generate_statistics_chart()
    with open(chart_path, 'rb') as img:
        bot.send_photo(chat_id=CHAT_ID, photo=img, caption=f"📊 *Performance Review*\nOwner: *Ankit Singh*")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("signal", signal))
    dp.add_handler(CommandHandler("stats", stats))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
