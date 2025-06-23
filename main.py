import logging, random, datetime, pytz from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

from utils.pairs import all_pairs from utils.ai_learning import get_best_pairs from analysis.analysis import analyze_pair from reports.report_generator import generate_performance_chart from utils.result_handler import report_trade_result

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54' logging.basicConfig(level=logging.INFO) auto_signal_jobs = {}  # PER CHAT SIGNAL MANAGEMENT

def get_future_entry_time(mins_ahead=1): tz = pytz.timezone("Asia/Kolkata") now = datetime.datetime.now(tz) next_minute = (now + datetime.timedelta(minutes=mins_ahead)).replace(second=0, microsecond=0) return next_minute.strftime("%H:%M:%S")

def start(update: Update, context: CallbackContext): buttons = [ [InlineKeyboardButton("📊 Daily Stats", callback_data='stats_daily')], [InlineKeyboardButton("📅 Monthly Stats", callback_data='stats_monthly')], [InlineKeyboardButton("📌 Custom Signal", callback_data='custom_signal')], [InlineKeyboardButton("🚀 Start Auto Signals", callback_data='start_auto')], [InlineKeyboardButton("🛑 Stop Auto Signals", callback_data='stop_auto')], ] update.message.reply_text( "👋 Welcome to Quotex Advanced Bot\n\nChoose an option:", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(buttons) )

def generate_signal(): while True: pair = random.choice(get_best_pairs(all_pairs)) result = analyze_pair(pair, None) if result['accuracy'] >= 90 and result['trend'] != 'Sideways': break

entry_time = get_future_entry_time(1)

return f"""👑 *Upcoming Quotex Signal* 👑

📌 Asset: {result['pair']} 🕐 Timeframe: 1 Minute 🎯 ENTRY at → {entry_time} (IST) 📉 Direction: {'⬆️ UP' if result['signal'] == 'UP' else '⬇️ DOWN'} 🌐 Trend: {result['trend']} 📊 Forecast Accuracy: {result['accuracy']}% 💰 Payout Rate: {result['payout']}%

📝 Strategy Logic: {result['logic']}

🇮🇳 All times are in IST (Asia/Kolkata) 💸 Follow Proper Money Management ⏳ Always Select 1 Minute Time Frame. """

def send_auto_signal(context: CallbackContext): chat_id = context.job.context signal_text = generate_signal() context.bot.send_message(chat_id=chat_id, text=signal_text, parse_mode='Markdown')

# Extract asset & direction for result reporting
lines = signal_text.splitlines()
asset_line = next((line for line in lines if "*Asset:*" in line), "")
direction_line = next((line for line in lines if "*Direction:*" in line), "")

asset = asset_line.replace("📌 *Asset:* ", "").strip()
direction = direction_line.replace("📉 *Direction:* ", "").replace("⬆️ ", "").replace("⬇️ ", "").replace("*", "").strip()

report_trade_result(context.bot, chat_id, asset, direction)

def start_auto(update: Update, context: CallbackContext): chat_id = update.effective_chat.id if chat_id in auto_signal_jobs: update.callback_query.edit_message_text("⚙️ Auto signals are already running in this chat!") return

job = context.job_queue.run_repeating(send_auto_signal, interval=60, first=0, context=chat_id)
auto_signal_jobs[chat_id] = job
update.callback_query.edit_message_text("✅ Auto signals started for this chat!")

def stop_auto(update: Update, context: CallbackContext): chat_id = update.effective_chat.id if chat_id in auto_signal_jobs: auto_signal_jobs[chat_id].schedule_removal() del auto_signal_jobs[chat_id] update.callback_query.edit_message_text("🛑 Auto signals stopped for this chat!") else: update.callback_query.edit_message_text("⚠️ No auto signals are running in this chat.")

def send_stats(update: Update, context: CallbackContext, period='daily'): wins = random.randint(20, 40) losses = random.randint(5, 15) accuracy = round((wins / (wins + losses)) * 100, 2) img = generate_performance_chart(wins, losses, accuracy, period) performance = "GOOD" if accuracy >= 80 else "AVERAGE" if accuracy >= 60 else "BAD" context.bot.send_photo( chat_id=update.effective_chat.id, photo=img, caption=f"""📊 {period.capitalize()} Performance

Wins: {wins} Losses: {losses} Accuracy: {accuracy}% Performance: {performance}""", parse_mode='Markdown' )

def button_handler(update: Update, context: CallbackContext): query = update.callback_query query.answer() if query.data == 'start_auto': start_auto(update, context) elif query.data == 'stop_auto': stop_auto(update, context) elif query.data == 'custom_signal': query.edit_message_text(text=generate_signal(), parse_mode='Markdown') elif query.data == 'stats_daily': send_stats(update, context, period='daily') elif query.data == 'stats_monthly': send_stats(update, context, period='monthly')

def main(): updater = Updater(TOKEN, use_context=True) dp = updater.dispatcher dp.add_handler(CommandHandler("start", start)) dp.add_handler(CallbackQueryHandler(button_handler)) updater.start_polling() updater.idle()

if name == "main": main()

               
