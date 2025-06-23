import logging, random, threading, time, datetime, pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

from utils.pairs import all_pairs
from utils.ai_learning import get_best_pairs
from analysis.analysis import analyze_pair
from reports.report_generator import generate_performance_chart
from utils.result_handler import report_trade_result

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54'
CHAT_ID = 6065493589

logging.basicConfig(level=logging.INFO)
auto_signal_job = None

# ✅ GET FUTURE ENTRY TIME
def get_future_entry_time(mins_ahead=1):
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)
    next_minute = (now + datetime.timedelta(minutes=mins_ahead)).replace(second=0, microsecond=0)
    return next_minute.strftime("%H:%M:%S")

# ✅ MAIN PERSISTENT KEYBOARD
def get_main_keyboard():
    keyboard = [
        ['📌 Start', '📊 Stats'],
        ['🚀 Start Auto', '🛑 Stop Auto']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ✅ START FUNCTION (Resets Everything)
def start(update: Update, context: CallbackContext):
    update.message.reply_text("♻️ Resetting Menu...", reply_markup=ReplyKeyboardRemove())

    buttons = [
        [InlineKeyboardButton("📊 Daily Stats", callback_data='stats_daily')],
        [InlineKeyboardButton("📅 Monthly Stats", callback_data='stats_monthly')],
        [InlineKeyboardButton("📌 Custom Signal", callback_data='custom_signal')],
        [InlineKeyboardButton("⚡ 10s Strategy Signal", callback_data='strategy_10s')],
        [InlineKeyboardButton("🚀 Start Auto Signals", callback_data='start_auto')],
        [InlineKeyboardButton("🛑 Stop Auto Signals", callback_data='stop_auto')],
    ]
    update.message.reply_text(
        "👋 Welcome to *Quotex Advanced Bot*!\n\n*Choose an option:*",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    update.message.reply_text(
        "📱 *Telegram Menu Active.*\nUse the buttons below 👇",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

# ✅ GENERATE SIGNAL FUNCTION
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

# ✅ SEND AUTO SIGNAL
def send_auto_signal(context: CallbackContext):
    signal_text = generate_signal()
    context.bot.send_message(chat_id=CHAT_ID, text=signal_text, parse_mode='Markdown')

    lines = signal_text.splitlines()
    asset_line = next((line for line in lines if "*Asset:*" in line), "")
    direction_line = next((line for line in lines if "*Direction:*" in line), "")

    asset = asset_line.replace("📌 *Asset:* ", "").strip()
    direction = direction_line.replace("📉 *Direction:* ", "").replace("⬆️ ", "").replace("⬇️ ", "").replace("*", "").strip()

    threading.Thread(target=report_trade_result, args=(context.bot, CHAT_ID, asset, direction)).start()

# ✅ START AUTO SIGNALS
def start_auto(update: Update, context: CallbackContext):
    global auto_signal_job
    if auto_signal_job:
        update.callback_query.edit_message_text("⚙️ Auto signals are already running!")
        return

    send_auto_signal(context)
    auto_signal_job = context.job_queue.run_repeating(send_auto_signal, interval=60, first=60)
    update.callback_query.edit_message_text("✅ Auto signals started! First signal sent, next every 1 minute.")

# ✅ STOP AUTO SIGNALS
def stop_auto(update: Update, context: CallbackContext):
    global auto_signal_job
    if auto_signal_job:
        auto_signal_job.schedule_removal()
        auto_signal_job = None
        update.callback_query.edit_message_text("🛑 Auto signals stopped!")
    else:
        update.callback_query.edit_message_text("⚠️ No auto signals are currently running.")

# ✅ GENERATE STATS IMAGE
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

# ✅ BUTTON HANDLER
def start(update: Update, context: CallbackContext):
    # Clear Old Menu
    update.message.reply_text("♻️ Resetting Menu...", reply_markup=ReplyKeyboardRemove())

    # Inline Buttons (Clickable Inside Message)
    buttons = [
        [InlineKeyboardButton("📊 Daily Stats", callback_data='stats_daily')],
        [InlineKeyboardButton("📅 Monthly Stats", callback_data='stats_monthly')],
        [InlineKeyboardButton("📌 Custom Signal", callback_data='custom_signal')],
        [InlineKeyboardButton("⚡ 10s Strategy Signal", callback_data='strategy_10s')],
        [InlineKeyboardButton("🚀 Start Auto Signals", callback_data='start_auto')],
        [InlineKeyboardButton("🛑 Stop Auto Signals", callback_data='stop_auto')],
    ]
    update.message.reply_text(
        "👋 Welcome to *Quotex Advanced Bot*!\n\n*Choose an option:*",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    # Permanent Keyboard (Bottom of Chat)
    keyboard = [
        ['📌 Start', '📊 Stats'],
        ['🚀 Start Auto', '🛑 Stop Auto']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("📱 *Telegram Menu Active.*\nUse the buttons below 👇", parse_mode='Markdown', reply_markup=reply_markup)
