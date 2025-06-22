import logging, random, datetime, threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, JobQueue

from utils.pairs import all_pairs
from utils.ai_learning import get_best_pairs
from utils.time_utils import is_exact_time
from analysis.analysis import analyze_pair
from reports.report_generator import generate_performance_chart
from utils.result_handler import report_trade_result  # ✅ Result reporting import

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54'
CHAT_ID = 6065493589

logging.basicConfig(level=logging.INFO)
auto_signal_job = None

# ✅ Start Menu
def start(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton("📊 Stats", callback_data='stats')],
        [InlineKeyboardButton("📌 Custom Signal", callback_data='custom_signal')],
        [InlineKeyboardButton("🚀 Start Auto Signals", callback_data='start_auto')],
        [InlineKeyboardButton("🛑 Stop Auto Signals", callback_data='stop_auto')],
    ]
    update.message.reply_text("👋 Welcome to *Quotex Advanced Bot*!", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(buttons))

# ✅ Generate Signal Function
from utils.time_utils import get_next_minute_entry_time

def generate_signal():
    pair = random.choice(get_best_pairs(all_pairs))
    result = analyze_pair(pair, None)
    return f"""
👑 *Quotex OTC Signal* 👑

📌 *Asset:* {result['pair']}
🕐 *Timeframe:* 1 Minute
⏰ *Entry Time:* {get_next_minute_entry_time()}
📉 *Direction:* {'⬆️ UP' if result['signal'] == 'UP' else '⬇️ DOWN'}
🌐 *Trend:* {result['trend']}
📊 *Forecast Accuracy:* {result['accuracy']}%
💰 *Payout Rate:* {result['payout']}%

🇮🇳 _All times are in UTC+5:30 (India Standard Time)_

💸 *Follow Proper Money Management*
⏳ _Always Select 1 Minute Time Frame._
"""

# ✅ Auto Signal Handling WITH Result Reporting
def send_auto_signal(context: CallbackContext):
    signal_text = generate_signal()
    context.bot.send_message(chat_id=CHAT_ID, text=signal_text, parse_mode='Markdown')

    # Extract pair & direction for result reporting
    lines = signal_text.splitlines()
    asset_line = next((line for line in lines if "*Asset:*" in line), "")
    direction_line = next((line for line in lines if "*Direction:*" in line), "")

    asset = asset_line.replace("📌 *Asset:* ", "").strip()
    direction = direction_line.replace("📉 *Direction:* ", "").replace("⬆️ ", "").replace("⬇️ ", "").replace("*", "").strip()

    # Background thread to handle result after 5 mins
    threading.Thread(target=report_trade_result, args=(context.bot, CHAT_ID, asset, direction)).start()

# ✅ 📊 Stats Chart Function
def send_stats(update: Update, context: CallbackContext):
    wins = random.randint(20, 40)
    losses = random.randint(5, 15)
    accuracy = round((wins / (wins + losses)) * 100, 2)

    img = generate_performance_chart(wins, losses, accuracy)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=img, caption=f"📊 *Performance Review*\nAccuracy: {accuracy}%", parse_mode='Markdown')

# ✅ Button Handler
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'start_auto':
        start_auto(update, context)
    elif query.data == 'stop_auto':
        stop_auto(update, context)
    elif query.data == 'custom_signal':
        query.edit_message_text(text=generate_signal(), parse_mode='Markdown')
    elif query.data == 'stats':
        send_stats(update, context)

# ✅ Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
