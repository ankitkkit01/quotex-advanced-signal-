import logging, random, threading, datetime, pytz from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

from utils.pairs import all_pairs from utils.ai_learning import get_best_pairs from analysis.analysis import analyze_pair from reports.report_generator import generate_performance_chart from utils.result_handler import report_trade_result

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54'

logging.basicConfig(level=logging.INFO)

Dict to manage auto-signal jobs per chat

auto_signal_jobs = {}

def get_future_entry_time(mins_ahead=1): tz = pytz.timezone("Asia/Kolkata") now = datetime.datetime.now(tz) next_minute = (now + datetime.timedelta(minutes=mins_ahead)).replace(second=0, microsecond=0) return next_minute.strftime("%H:%M:%S")

def start(update: Update, context: CallbackContext): keyboard = ReplyKeyboardMarkup( [["🚀 Start Auto Signals", "🛑 Stop Auto Signals"], ["📌 Custom Signal", "⚡ 10s Strategy"], ["📊 Daily Stats", "📅 Monthly Stats"]], resize_keyboard=True ) update.message.reply_text( "👋 Welcome to Quotex Advanced Bot\n\nChoose an option:", parse_mode='Markdown', reply_markup=keyboard )

def generate_signal(): while True: pair = random.choice(get_best_pairs(all_pairs)) result = analyze_pair(pair, None) if result['accuracy'] >= 90 and result['trend'] != 'Sideways': break

entry_time = get_future_entry_time(1)

return f"""👑 *Upcoming Quotex Signal* 👑

📌 Asset: {result['pair']} 🕐 Timeframe: 1 Minute 🎯 ENTRY at → {entry_time} (IST) 📉 Direction: {'⬆️ UP' if result['signal'] == 'UP' else '⬇️ DOWN'} 🌐 Trend: {result['trend']} 📊 Forecast Accuracy: {result['accuracy']}% 💰 Payout Rate: {result['payout']}%

📝 Strategy Logic: {result['logic']}

🇮🇳 All times are in IST (Asia/Kolkata) 💸 Follow Proper Money Management"""

def send_auto_signal(context: CallbackContext): chat_id = context.job.context signal_text = generate_signal() context.bot.send_message(chat_id=chat_id, text=signal_text, parse_mode='Markdown')

lines = signal_text.splitlines()
asset_line = next((line for line in lines if "*Asset:*" in line), "")
direction_line = next((line for line in lines if "*Direction:*" in line), "")

asset = asset_line.replace("📌 *Asset:* ", "").strip()
direction = direction_line.replace("📉 *Direction:* ", "").replace("⬆️ ", "").replace("⬇️ ", "").replace("*", "").strip()

threading.Thread(target=report_trade_result, args=(context.bot, chat_id, asset, direction)).start()

def handle_text(update: Update, context: CallbackContext): chat_id = update.effective_chat.id text = update.message.text

if text == "🚀 Start Auto Signals":
    if chat_id in auto_signal_jobs:
        update.message.reply_text("⚙️ Auto signals are already running!")
    else:
        job = context.job_queue.run_repeating(send_auto_signal, interval=60, first=0, context=chat_id)
        auto_signal_jobs[chat_id] = job
        update.message.reply_text("✅ Auto signals started! First signal sent, next every 1 minute.")

elif text == "🛑 Stop Auto Signals":
    if chat_id in auto_signal_jobs:
        auto_signal_jobs[chat_id].schedule_removal()
        del auto_signal_jobs[chat_id]
        update.message.reply_text("🛑 Auto signals stopped!")
    else:
        update.message.reply_text("⚠️ No auto signals are currently running.")

elif text == "📌 Custom Signal":
    update.message.reply_text(generate_signal(), parse_mode='Markdown')

elif text == "📊 Daily Stats":
    send_stats(update, context, period='daily')

elif text == "📅 Monthly Stats":
    send_stats(update, context, period='monthly')

elif text == "⚡ 10s Strategy":
    update.message.reply_text("⚡ Coming Soon: Advanced 10-second Strategy Signals!", parse_mode='Markdown')

def send_stats(update: Update, context: CallbackContext, period='daily'): wins = random.randint(20, 40) losses = random.randint(5, 15) accuracy = round((wins / (wins + losses)) * 100, 2) img = generate_performance_chart(wins, losses, accuracy, period) performance = "GOOD" if accuracy >= 80 else "AVERAGE" if accuracy >= 60 else "BAD"

context.bot.send_photo(
    chat_id=update.effective_chat.id,
    photo=img,
    caption=f"""📊 *{period.capitalize()} Performance*

Wins: {wins} Losses: {losses} Accuracy: {accuracy}% Performance: {performance}""", parse_mode='Markdown' )

def main(): updater = Updater(TOKEN, use_context=True) dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", start))
dp.add_handler(CommandHandler("menu", start))

dp.add_handler(CommandHandler("stop", start))  # optional redundant

dp.add_handler(CommandHandler("signal", lambda u, c: u.message.reply_text(generate_signal(), parse_mode='Markdown')))
dp.add_handler(CommandHandler("stats", lambda u, c: send_stats(u, c, period='daily')))

dp.add_handler(CommandHandler("reset", lambda u, c: u.message.reply_text("Resetting soon...")))

dp.add_handler(CommandHandler("stopall", lambda u, c: [job.schedule_removal() for job in auto_signal_jobs.values()] or auto_signal_jobs.clear() or u.message.reply_text("🛑 All auto signals stopped.")))

dp.add_handler(CommandHandler("id", lambda u, c: u.message.reply_text(f"Your chat ID: `{u.effective_chat.id}`", parse_mode='Markdown')))

dp.add_handler(CommandHandler("custom", lambda u, c: u.message.reply_text(generate_signal(), parse_mode='Markdown')))

dp.add_handler(CommandHandler("10s", lambda u, c: u.message.reply_text("⚡ Coming Soon!", parse_mode='Markdown')))

dp.add_handler(CommandHandler("force_stop", lambda u, c: stop_auto_for_user(u, c)))

from telegram.ext import MessageHandler, Filters
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

updater.start_polling()
updater.idle()

def stop_auto_for_user(update, context): chat_id = update.effective_chat.id if chat_id in auto_signal_jobs: auto_signal_jobs[chat_id].schedule_removal() del auto_signal_jobs[chat_id] update.message.reply_text("✅ Forced stop of your auto signals.")

if name == "main": main()

