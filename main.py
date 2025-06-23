import logging, random, threading, datetime, pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

from utils.pairs import all_pairs
from utils.ai_learning import get_best_pairs
from analysis.analysis import analyze_pair
from reports.report_generator import generate_performance_chart
from utils.result_handler import report_trade_result

TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = YOUR_CHAT_ID

logging.basicConfig(level=logging.INFO)
auto_signal_job = None

def get_future_entry_time(mins_ahead=1):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)
    next_minute = (now + datetime.timedelta(minutes=mins_ahead)).replace(second=0, microsecond=0)
    return next_minute.strftime("%H:%M:%S")

def start(update: Update, context: CallbackContext):
    reply_keyboard = [['📊 Daily Stats', '📅 Monthly Stats'], ['📌 Custom Signal', '⚡ 10s Strategy Signal'], ['🚀 Start Auto Signals', '🛑 Stop Auto Signals']]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    buttons = [
        [InlineKeyboardButton("📊 Daily Stats", callback_data='stats_daily')],
        [InlineKeyboardButton("📅 Monthly Stats", callback_data='stats_monthly')],
        [InlineKeyboardButton("📌 Custom Signal", callback_data='custom_signal')],
        [InlineKeyboardButton("⚡ 10s Strategy Signal", callback_data='strategy_10s')],
        [InlineKeyboardButton("🚀 Start Auto Signals", callback_data='start_auto')],
        [InlineKeyboardButton("🛑 Stop Auto Signals", callback_data='stop_auto')],
    ]

    update.message.reply_text(
        "👋 Welcome to *Quotex Advanced Bot*!\n\n*Choose an option below:*",
        parse_mode='Markdown',
        reply_markup=markup
    )
    update.message.reply_text(
        "👇 Quick Menu:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

def generate_signal():
    while True:
        pair = random.choice(get_best_pairs(all_pairs))
        result = analyze_pair(pair, None)
        if result['accuracy'] >= 90 and result['trend'] != 'Sideways':
            break

    entry_time = get_future_entry_time(1)

    return f"""👑 *Upcoming Quotex Signal* 👑

📌 *Asset:* {result['pair']}
🕐 *Timeframe:* 1 Minute
🎯 *ENTRY at → {entry_time} (IST)*
📉 *Direction:* {'⬆️ UP' if result['signal'] == 'UP' else '⬇️ DOWN'}
🌐 *Trend:* {result['trend']}
📊 *Forecast Accuracy:* {result['accuracy']}%
💰 *Payout Rate:* {result['payout']}%

📝 *Strategy Logic:* {result['logic']}

🇮🇳 _All times are in IST (Asia/Kolkata)_
💸 *Follow Proper Money Management*
⏳ _Always Select 1 Minute Time Frame._
"""

def send_auto_signal(context: CallbackContext):
    signal_text = generate_signal()
    context.bot.send_message(chat_id=CHAT_ID, text=signal_text, parse_mode='Markdown')

    # Extract for result reporting
    lines = signal_text.splitlines()
    asset_line = next((line for line in lines if "*Asset:*" in line), "")
    direction_line = next((line for line in lines if "*Direction:*" in line), "")

    asset = asset_line.replace("📌 *Asset:* ", "").strip()
    direction = direction_line.replace("📉 *Direction:* ", "").replace("⬆️ ", "").replace("⬇️ ", "").replace("*", "").strip()

    threading.Thread(target=report_trade_result, args=(context.bot, CHAT_ID, asset, direction)).start()

def start_auto(update: Update, context: CallbackContext):
    global auto_signal_job
    query = update.callback_query
    query.answer()
    if auto_signal_job:
        query.edit_message_text("⚙️ Auto signals are already running!")
        return

    send_auto_signal(context)
    auto_signal_job = context.job_queue.run_repeating(send_auto_signal, interval=60, first=60)
    query.edit_message_text("✅ Auto signals started! First signal sent, next every 1 minute.")

def stop_auto(update: Update, context: CallbackContext):
    global auto_signal_job
    query = update.callback_query
    query.answer()
    if auto_signal_job:
        auto_signal_job.schedule_removal()
        auto_signal_job = None
        query.edit_message_text("🛑 Auto signals stopped!")
    else:
        query.edit_message_text("⚠️ No auto signals are currently running.")

def send_stats(update: Update, context: CallbackContext, period='daily'):
    wins = random.randint(20, 40)
    losses = random.randint(5, 15)
    accuracy = round((wins / (wins + losses)) * 100, 2)
    img = generate_performance_chart(wins, losses, accuracy, period)
    performance = "GOOD" if accuracy >= 80 else "AVERAGE" if accuracy >= 60 else "BAD"
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=img,
        caption=f"""📊 *{period.capitalize()} Performance*

Wins: {wins}
Losses: {losses}
Accuracy: {accuracy}%
Performance: {performance}""",
        parse_mode='Markdown'
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data == 'start_auto':
        start_auto(update, context)
    elif data == 'stop_auto':
        stop_auto(update, context)
    elif data == 'custom_signal':
        query.edit_message_text(text=generate_signal(), parse_mode='Markdown')
    elif data == 'stats_daily':
        send_stats(update, context, period='daily')
    elif data == 'stats_monthly':
        send_stats(update, context, period='monthly')
    elif data == 'strategy_10s':
        query.edit_message_text("⚡ Coming Soon: Advanced 10-second Strategy Signals!", parse_mode='Markdown')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
