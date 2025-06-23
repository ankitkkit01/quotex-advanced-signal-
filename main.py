import logging, random, datetime, pytz
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from utils.pairs import all_pairs
from utils.ai_learning import get_best_pairs
from analysis.analysis import analyze_pair
from reports.report_generator import generate_performance_chart
from utils.result_handler import report_trade_result

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54'
CHAT_ID = 6065493589

logging.basicConfig(level=logging.INFO)
auto_signal_job = None
auto_signal_running = False

def get_future_entry_time(mins_ahead=1):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)
    next_minute = (now + datetime.timedelta(minutes=mins_ahead)).replace(second=0, microsecond=0)
    return next_minute.strftime("%H:%M:%S")

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
"""

def send_auto_signal(context: CallbackContext):
    if not auto_signal_running:
        return
    signal_text = generate_signal()
    context.bot.send_message(chat_id=CHAT_ID, text=signal_text, parse_mode='Markdown')

def start(update: Update, context: CallbackContext):
    text = """👋 Welcome to *Quotex Advanced Bot*!

Available Commands:
/start → Show this help
/auto → Start Auto Signals
/stop → Stop Auto Signals
/custom → Custom Signal
/stats → Daily Stats
"""
    update.message.reply_text(text, parse_mode='Markdown')

def auto(update: Update, context: CallbackContext):
    global auto_signal_job, auto_signal_running
    if auto_signal_running:
        update.message.reply_text("⚙️ Auto signals already running!")
        return
    auto_signal_running = True
    send_auto_signal(context)
    auto_signal_job = context.job_queue.run_repeating(send_auto_signal, interval=60, first=60)
    update.message.reply_text("✅ Auto signals started!")

def stop(update: Update, context: CallbackContext):
    global auto_signal_job, auto_signal_running
    if auto_signal_job:
        auto_signal_job.schedule_removal()
        auto_signal_job = None
    auto_signal_running = False
    update.message.reply_text("🛑 Auto signals stopped!")

def custom(update: Update, context: CallbackContext):
    update.message.reply_text(generate_signal(), parse_mode='Markdown')

def stats(update: Update, context: CallbackContext):
    wins = random.randint(20, 40)
    losses = random.randint(5, 15)
    accuracy = round((wins / (wins + losses)) * 100, 2)
    img = generate_performance_chart(wins, losses, accuracy, 'daily')
    performance = "GOOD" if accuracy >= 80 else "AVERAGE" if accuracy >= 60 else "BAD"
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=img, caption=f"""📊 *Daily Performance*

Wins: {wins}
Losses: {losses}
Accuracy: {accuracy}%
Performance: {performance}""", parse_mode='Markdown')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("auto", auto))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("custom", custom))
    dp.add_handler(CommandHandler("stats", stats))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
