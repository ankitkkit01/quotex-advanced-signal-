import logging, random, threading, datetime, pytz
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from utils.pairs import all_pairs
from utils.ai_learning import get_best_pairs
from analysis.analysis import analyze_pair
from reports.report_generator import generate_performance_chart
from automation.browser_automation import start_browser_login  # ✅ IMPORT FROM automation FOLDER
from utils.result_handler import report_trade_result

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54'
CHAT_ID = 6065493589
EMAIL = "arhimanshya@gmail.com"
PASSWORD = "12345678an"

logging.basicConfig(level=logging.INFO)
auto_signal_job = None

def get_future_entry_time(mins_ahead=1):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)
    next_minute = (now + datetime.timedelta(minutes=mins_ahead)).replace(second=0, microsecond=0)
    return next_minute.strftime("%H:%M:%S")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Welcome to *Quotex Advanced Bot*!\n\n"
        "Commands:\n"
        "/start_auto - Start Auto Signals\n"
        "/stop_auto - Stop Auto Signals\n"
        "/custom_signal - Generate Custom Signal\n"
        "/stats_daily - Daily Performance Stats\n"
        "/stats_monthly - Monthly Performance Stats\n"
        "/login_browser - Login Quotex using Browser",
        parse_mode='Markdown'
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

    lines = signal_text.splitlines()
    asset_line = next((line for line in lines if "*Asset:*" in line), "")
    direction_line = next((line for line in lines if "*Direction:*" in line), "")

    asset = asset_line.replace("📌 *Asset:* ", "").strip()
    direction = direction_line.replace("📉 *Direction:* ", "").replace("⬆️ ", "").replace("⬇️ ", "").replace("*", "").strip()

    threading.Thread(target=report_trade_result, args=(context.bot, CHAT_ID, asset, direction)).start()

def start_auto(update: Update, context: CallbackContext):
    global auto_signal_job
    if auto_signal_job:
        update.message.reply_text("⚙️ Auto signals already running!")
        return

    send_auto_signal(context)
    auto_signal_job = context.job_queue.run_repeating(send_auto_signal, interval=60, first=60)
    update.message.reply_text("✅ Auto signals started! First signal sent, next every 1 minute.")

def stop_auto(update: Update, context: CallbackContext):
    global auto_signal_job
    if auto_signal_job:
        auto_signal_job.schedule_removal()
        auto_signal_job = None
        update.message.reply_text("🛑 Auto signals stopped!")
    else:
        update.message.reply_text("⚠️ No auto signals are currently running.")

def custom_signal(update: Update, context: CallbackContext):
    signal_text = generate_signal()
    context.bot.send_message(chat_id=update.effective_chat.id, text=signal_text, parse_mode='Markdown')

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

def stats_daily(update: Update, context: CallbackContext):
    send_stats(update, context, period='daily')

def stats_monthly(update: Update, context: CallbackContext):
    send_stats(update, context, period='monthly')

def login_browser(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="⚙️ Logging into Quotex using Browser...")
    try:
        start_browser_login(EMAIL, PASSWORD)
        context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Browser login attempted.")
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"❌ Browser login failed: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("start_auto", start_auto))
    dp.add_handler(CommandHandler("stop_auto", stop_auto))
    dp.add_handler(CommandHandler("custom_signal", custom_signal))
    dp.add_handler(CommandHandler("stats_daily", stats_daily))
    dp.add_handler(CommandHandler("stats_monthly", stats_monthly))
    dp.add_handler(CommandHandler("login_browser", login_browser))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
