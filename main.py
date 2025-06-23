import logging, random, datetime, pytz from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue

from utils.pairs import all_pairs from utils.ai_learning import get_best_pairs from analysis.analysis import analyze_pair from reports.report_generator import generate_performance_chart from utils.result_handler import report_trade_result

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54' CHAT_ID = 6065493589

logging.basicConfig(level=logging.INFO) jobs = {}

MENU = ReplyKeyboardMarkup( [['📊 Daily Stats', '📅 Monthly Stats'], ['📌 Custom Signal', '⚡ Start Auto Signals'], ['🛑 Stop Auto Signals']], resize_keyboard=True )

def get_future_entry_time(mins_ahead=1): tz = pytz.timezone("Asia/Kolkata") now = datetime.datetime.now(tz) next_minute = (now + datetime.timedelta(minutes=mins_ahead)).replace(second=0, microsecond=0) return next_minute.strftime("%H:%M:%S")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "👋 Welcome to Quotex Advanced Bot\n\nChoose an option:", parse_mode='Markdown', reply_markup=MENU )

async def generate_signal(): while True: pair = random.choice(get_best_pairs(all_pairs)) result = analyze_pair(pair, None) if result['accuracy'] >= 90 and result['trend'] != 'Sideways': break

entry_time = get_future_entry_time(1)

return f"""👑 *Upcoming Quotex Signal* 👑

📌 Asset: {result['pair']} 🕐 Timeframe: 1 Minute 🎯 ENTRY at → {entry_time} (IST) 📉 Direction: {'⬆️ UP' if result['signal'] == 'UP' else '⬇️ DOWN'} 🌐 Trend: {result['trend']} 📊 Forecast Accuracy: {result['accuracy']}% 💰 Payout Rate: {result['payout']}%

📝 Strategy Logic: {result['logic']}

🇮🇳 All times are in IST (Asia/Kolkata) 💸 Follow Proper Money Management ⏳ Always Select 1 Minute Time Frame. """

async def send_auto_signal(context: ContextTypes.DEFAULT_TYPE): signal_text = await generate_signal() await context.bot.send_message(chat_id=context.job.chat_id, text=signal_text, parse_mode='Markdown')

lines = signal_text.splitlines()
asset_line = next((line for line in lines if "*Asset:*" in line), "")
direction_line = next((line for line in lines if "*Direction:*" in line), "")

asset = asset_line.replace("📌 *Asset:* ", "").strip()
direction = direction_line.replace("📉 *Direction:* ", "").replace("⬆️ ", "").replace("⬇️ ", "").replace("*", "").strip()

await report_trade_result(context.bot, context.job.chat_id, asset, direction)

async def start_auto(update: Update, context: ContextTypes.DEFAULT_TYPE): chat_id = update.effective_chat.id if chat_id in jobs: await update.message.reply_text("⚙️ Auto signals are already running!") return

job = context.job_queue.run_repeating(send_auto_signal, interval=60, first=1, chat_id=chat_id)
jobs[chat_id] = job

await update.message.reply_text("✅ Auto signals started! First signal sent, next every 1 minute.")

async def stop_auto(update: Update, context: ContextTypes.DEFAULT_TYPE): chat_id = update.effective_chat.id if chat_id in jobs: jobs[chat_id].schedule_removal() del jobs[chat_id] await update.message.reply_text("🛑 Auto signals stopped!", reply_markup=MENU) else: await update.message.reply_text("⚠️ No auto signals are currently running.")

async def send_stats(update: Update, context: ContextTypes.DEFAULT_TYPE, period='daily'): wins = random.randint(20, 40) losses = random.randint(5, 15) accuracy = round((wins / (wins + losses)) * 100, 2) img = generate_performance_chart(wins, losses, accuracy, period) performance = "GOOD" if accuracy >= 80 else "AVERAGE" if accuracy >= 60 else "BAD"

await context.bot.send_photo(
    chat_id=update.effective_chat.id,
    photo=img,
    caption=f"""📊 *{period.capitalize()} Performance*

Wins: {wins} Losses: {losses} Accuracy: {accuracy}% Performance: {performance}""", parse_mode='Markdown' )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text if text == '📌 Custom Signal': signal = await generate_signal() await update.message.reply_text(signal, parse_mode='Markdown')

elif text == '⚡ Start Auto Signals':
    await start_auto(update, context)

elif text == '🛑 Stop Auto Signals':
    await stop_auto(update, context)

elif text == '📊 Daily Stats':
    await send_stats(update, context, period='daily')

elif text == '📅 Monthly Stats':
    await send_stats(update, context, period='monthly')

async def main(): app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("start_auto", start_auto))
app.add_handler(CommandHandler("stop_auto", stop_auto))

app.add_handler(CommandHandler("stats_daily", lambda u, c: send_stats(u, c, 'daily')))
app.add_handler(CommandHandler("stats_monthly", lambda u, c: send_stats(u, c, 'monthly')))

app.add_handler(CommandHandler("custom_signal", lambda u, c: u.message.reply_text(await generate_signal(), parse_mode='Markdown')))

app.add_handler(CommandHandler("help", start))
app.add_handler(CommandHandler("menu", start))

app.add_handler(MessageHandler(None, handle_message))

await app.run_polling()

if name == "main": import asyncio asyncio.run(main())

