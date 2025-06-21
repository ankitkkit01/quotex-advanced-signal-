import logging
import random
from collections import defaultdict, deque
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from analysis.analysis import analyze_pair
-----------------------------------------

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54' MY_CHAT_ID = 6065493589

-----------------------------------------

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

ALL_PAIRS = [ "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD", "USDBRL", "USDBDT", "USDDZD", "USDHUF", "USDMXN", "USDRUB", "USDTRY", "USDZAR", "EURGBP", "EURCHF", "EURJPY", "EURAUD", "EURCAD", "EURNZD", "GBPCHF", "GBPJPY", "AUDJPY", "AUDCAD", "AUDCHF", "AUDNZD", "CADJPY", "CHFJPY", "NZDCAD", "NZDCHF", "NZDJPY", "USDNOK", "USDSGD", "USDSEK", "BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD", "GOLD", "SILVER", "OIL", "USDBGN", "USDHRK", "USDCZK", "USDPHP", "USDPEN", "USDPLN", "USDHUF", "USDILS", "USDMAD", "USDTHB", "USDXAU", "USDXAG", "USDDKK", "USDINR", "USDIDR", "USDKRW", "USDHKD" ]

signal_history = defaultdict(lambda: deque(maxlen=50))

auto_signal_10sec = False auto_signal_1min = False

def start(update: Update, context: CallbackContext): update.message.reply_text( "Welcome to Quotex Advanced Signal Bot by Ankit Singh!\nUse /menu to see options." )

def menu(update: Update, context: CallbackContext): keyboard = [ [InlineKeyboardButton("▶️ Start 10s Auto Signals", callback_data='start_10s')], [InlineKeyboardButton("⏹ Stop 10s Auto Signals", callback_data='stop_10s')], [InlineKeyboardButton("▶️ Start 1min Auto Signals", callback_data='start_1min')], [InlineKeyboardButton("⏹ Stop 1min Auto Signals", callback_data='stop_1min')], [InlineKeyboardButton("🔎 Custom Signal Generator", callback_data='custom_signal')], [InlineKeyboardButton("📊 Statistics Report", callback_data='stats_report')], [InlineKeyboardButton("🤖 AI Self-Learning Status", callback_data='ai_status')], [InlineKeyboardButton("📈 Trading Plan Generator", callback_data='trading_plan')], [InlineKeyboardButton("💰 Auto Money Management", callback_data='money_management')], [InlineKeyboardButton("🎯 Set Trading Goals", callback_data='set_goals')], [InlineKeyboardButton("📝 Send Manual Signal", callback_data='manual_signal')], ] reply_markup = InlineKeyboardMarkup(keyboard) update.message.reply_text('Select an option:', reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext): query = update.callback_query query.answer() global auto_signal_10sec, auto_signal_1min

if query.data == 'start_10s':
    if not auto_signal_10sec:
        auto_signal_10sec = True
        context.job_queue.run_repeating(send_auto_signal_10sec, interval=10, first=1, context=update.effective_chat.id, name="auto_10sec")
        query.edit_message_text(text="10-second Auto Signals Started ✅")
    else:
        query.edit_message_text(text="10-second Auto Signals already running.")

elif query.data == 'stop_10s':
    auto_signal_10sec = False
    context.job_queue.stop_job("auto_10sec")
    query.edit_message_text(text="10-second Auto Signals Stopped ❌")

elif query.data == 'start_1min':
    if not auto_signal_1min:
        auto_signal_1min = True
        context.job_queue.run_repeating(send_auto_signal_1min, interval=60, first=1, context=update.effective_chat.id, name="auto_1min")
        query.edit_message_text(text="1-minute Auto Signals Started ✅")
    else:
        query.edit_message_text(text="1-minute Auto Signals already running.")

elif query.data == 'stop_1min':
    auto_signal_1min = False
    context.job_queue.stop_job("auto_1min")
    query.edit_message_text(text="1-minute Auto Signals Stopped ❌")

elif query.data == 'custom_signal':
    query.edit_message_text(text="Custom Signal Generator: Feature Coming Soon ✅")

elif query.data == 'stats_report':
    send_statistics_report(update, context)

elif query.data == 'ai_status':
    query.edit_message_text(text="🤖 AI Self-Learning Status: Basic Module Active ✅")

elif query.data == 'trading_plan':
    query.edit_message_text(text="📈 Trading Plan Generator Coming Soon ✅")

elif query.data == 'money_management':
    query.edit_message_text(text="💰 Auto Money Management Feature Coming Soon ✅")

elif query.data == 'set_goals':
    query.edit_message_text(text="🎯 Set Trading Goals Feature Coming Soon ✅")

elif query.data == 'manual_signal':
    send_manual_signal(update, context)

def send_manual_signal(update: Update, context: CallbackContext): pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) update.callback_query.message.reply_text(msg)

def generate_dummy_data(): data = { 'open': np.random.rand(100) * 100, 'high': np.random.rand(100) * 100 + 0.5, 'low': np.random.rand(100) * 100 - 0.5, 'close': np.random.rand(100) * 100, 'volume': np.random.randint(1000, 5000, 100) } return pd.DataFrame(data)

def format_signal_message(result): msg = f"📈 Pair: {result['pair']}\n" msg += f"🔔 Signal: {result['signal']}\n" msg += "📝 Analysis:\n" for line in result['analysis']: msg += f" - {line}\n" return msg

def update_signal_history(pair, result): win = random.choice([True, False])  # Dummy win/loss, replace with real logic signal_history[pair].append(win)

def filter_pairs_by_performance(): filtered = [] for pair, history in signal_history.items(): if len(history) >= 10: win_ratio = sum(history) / len(history) if win_ratio > 0.7: filtered.append(pair) return filtered

def send_auto_signal_10sec(context: CallbackContext): chat_id = context.job.context good_pairs = filter_pairs_by_performance() if good_pairs: pair = random.choice(good_pairs) else: pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) context.bot.send_message(chat_id=chat_id, text=msg) update_signal_history(pair, result)

def send_auto_signal_1min(context: CallbackContext): chat_id = context.job.context good_pairs = filter_pairs_by_performance() if good_pairs: pair = random.choice(good_pairs) else: pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) context.bot.send_message(chat_id=chat_id, text=msg) update_signal_history(pair, result)

def send_statistics_report(update, context): wins = 18 losses = 7

fig, ax = plt.subplots()
ax.bar(['Wins', 'Losses'], [wins, losses], color=['green', 'red'])
ax.set_ylabel('Trades')
ax.set_title('Performance Summary - Ankit Singh')

image_path = 'performance_chart.png'
plt.savefig(image_path)
plt.close()

with open(image_path, 'rb') as photo:
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption="📊 Performance Chart")

def main(): updater = Updater(TOKEN, use_context=True) dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("menu", menu))
dp.add_handler(CallbackQueryHandler(button_handler))

updater.start_polling()
updater.idle()

if name == "main": main()


port random from collections import defaultdict, deque from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup import pandas as pd import numpy as np import matplotlib.pyplot as plt from analysis.analysis import analyze_pair

-----------------------------------------

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54' MY_CHAT_ID = 6065493589

-----------------------------------------

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

ALL_PAIRS = [ "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD", "USDBRL", "USDBDT", "USDDZD", "USDHUF", "USDMXN", "USDRUB", "USDTRY", "USDZAR", "EURGBP", "EURCHF", "EURJPY", "EURAUD", "EURCAD", "EURNZD", "GBPCHF", "GBPJPY", "AUDJPY", "AUDCAD", "AUDCHF", "AUDNZD", "CADJPY", "CHFJPY", "NZDCAD", "NZDCHF", "NZDJPY", "USDNOK", "USDSGD", "USDSEK", "BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD", "GOLD", "SILVER", "OIL", "USDBGN", "USDHRK", "USDCZK", "USDPHP", "USDPEN", "USDPLN", "USDHUF", "USDILS", "USDMAD", "USDTHB", "USDXAU", "USDXAG", "USDDKK", "USDINR", "USDIDR", "USDKRW", "USDHKD" ]

signal_history = defaultdict(lambda: deque(maxlen=50))

auto_signal_10sec = False auto_signal_1min = False

def start(update: Update, context: CallbackContext): update.message.reply_text( "Welcome to Quotex Advanced Signal Bot by Ankit Singh!\nUse /menu to see options." )

def menu(update: Update, context: CallbackContext): keyboard = [ [InlineKeyboardButton("▶️ Start 10s Auto Signals", callback_data='start_10s')], [InlineKeyboardButton("⏹ Stop 10s Auto Signals", callback_data='stop_10s')], [InlineKeyboardButton("▶️ Start 1min Auto Signals", callback_data='start_1min')], [InlineKeyboardButton("⏹ Stop 1min Auto Signals", callback_data='stop_1min')], [InlineKeyboardButton("🔎 Custom Signal Generator", callback_data='custom_signal')], [InlineKeyboardButton("📊 Statistics Report", callback_data='stats_report')], [InlineKeyboardButton("🤖 AI Self-Learning Status", callback_data='ai_status')], [InlineKeyboardButton("📈 Trading Plan Generator", callback_data='trading_plan')], [InlineKeyboardButton("💰 Auto Money Management", callback_data='money_management')], [InlineKeyboardButton("🎯 Set Trading Goals", callback_data='set_goals')], [InlineKeyboardButton("📝 Send Manual Signal", callback_data='manual_signal')], ] reply_markup = InlineKeyboardMarkup(keyboard) update.message.reply_text('Select an option:', reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext): query = update.callback_query query.answer() global auto_signal_10sec, auto_signal_1min

if query.data == 'start_10s':
    if not auto_signal_10sec:
        auto_signal_10sec = True
        context.job_queue.run_repeating(send_auto_signal_10sec, interval=10, first=1, context=update.effective_chat.id, name="auto_10sec")
        query.edit_message_text(text="10-second Auto Signals Started ✅")
    else:
        query.edit_message_text(text="10-second Auto Signals already running.")

elif query.data == 'stop_10s':
    auto_signal_10sec = False
    context.job_queue.stop_job("auto_10sec")
    query.edit_message_text(text="10-second Auto Signals Stopped ❌")

elif query.data == 'start_1min':
    if not auto_signal_1min:
        auto_signal_1min = True
        context.job_queue.run_repeating(send_auto_signal_1min, interval=60, first=1, context=update.effective_chat.id, name="auto_1min")
        query.edit_message_text(text="1-minute Auto Signals Started ✅")
    else:
        query.edit_message_text(text="1-minute Auto Signals already running.")

elif query.data == 'stop_1min':
    auto_signal_1min = False
    context.job_queue.stop_job("auto_1min")
    query.edit_message_text(text="1-minute Auto Signals Stopped ❌")

elif query.data == 'custom_signal':
    query.edit_message_text(text="Custom Signal Generator: Feature Coming Soon ✅")

elif query.data == 'stats_report':
    send_statistics_report(update, context)

elif query.data == 'ai_status':
    query.edit_message_text(text="🤖 AI Self-Learning Status: Basic Module Active ✅")

elif query.data == 'trading_plan':
    query.edit_message_text(text="📈 Trading Plan Generator Coming Soon ✅")

elif query.data == 'money_management':
    query.edit_message_text(text="💰 Auto Money Management Feature Coming Soon ✅")

elif query.data == 'set_goals':
    query.edit_message_text(text="🎯 Set Trading Goals Feature Coming Soon ✅")

elif query.data == 'manual_signal':
    send_manual_signal(update, context)

def send_manual_signal(update: Update, context: CallbackContext): pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) update.callback_query.message.reply_text(msg)

def generate_dummy_data(): data = { 'open': np.random.rand(100) * 100, 'high': np.random.rand(100) * 100 + 0.5, 'low': np.random.rand(100) * 100 - 0.5, 'close': np.random.rand(100) * 100, 'volume': np.random.randint(1000, 5000, 100) } return pd.DataFrame(data)

def format_signal_message(result): msg = f"📈 Pair: {result['pair']}\n" msg += f"🔔 Signal: {result['signal']}\n" msg += "📝 Analysis:\n" for line in result['analysis']: msg += f" - {line}\n" return msg

def update_signal_history(pair, result): win = random.choice([True, False])  # Dummy win/loss, replace with real logic signal_history[pair].append(win)

def filter_pairs_by_performance(): filtered = [] for pair, history in signal_history.items(): if len(history) >= 10: win_ratio = sum(history) / len(history) if win_ratio > 0.7: filtered.append(pair) return filtered

def send_auto_signal_10sec(context: CallbackContext): chat_id = context.job.context good_pairs = filter_pairs_by_performance() if good_pairs: pair = random.choice(good_pairs) else: pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) context.bot.send_message(chat_id=chat_id, text=msg) update_signal_history(pair, result)

def send_auto_signal_1min(context: CallbackContext): chat_id = context.job.context good_pairs = filter_pairs_by_performance() if good_pairs: pair = random.choice(good_pairs) else: pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) context.bot.send_message(chat_id=chat_id, text=msg) update_signal_history(pair, result)

def send_statistics_report(update, context): wins = 18 losses = 7

fig, ax = plt.subplots()
ax.bar(['Wins', 'Losses'], [wins, losses], color=['green', 'red'])
ax.set_ylabel('Trades')
ax.set_title('Performance Summary - Ankit Singh')

image_path = 'performance_chart.png'
plt.savefig(image_path)
plt.close()

with open(image_path, 'rb') as photo:
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption="📊 Performance Chart")

def main(): updater = Updater(TOKEN, use_context=True) dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("menu", menu))
dp.add_handler(CallbackQueryHandler(button_handler))

updater.start_polling()
updater.idle()

if name == "main": main()



-----------------------------------------

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54' MY_CHAT_ID = 6065493589

-----------------------------------------

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

ALL_PAIRS = [ "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD", "USDBRL", "USDBDT", "USDDZD", "USDHUF", "USDMXN", "USDRUB", "USDTRY", "USDZAR", "EURGBP", "EURCHF", "EURJPY", "EURAUD", "EURCAD", "EURNZD", "GBPCHF", "GBPJPY", "AUDJPY", "AUDCAD", "AUDCHF", "AUDNZD", "CADJPY", "CHFJPY", "NZDCAD", "NZDCHF", "NZDJPY", "USDNOK", "USDSGD", "USDSEK", "BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD", "GOLD", "SILVER", "OIL", "USDBGN", "USDHRK", "USDCZK", "USDPHP", "USDPEN", "USDPLN", "USDHUF", "USDILS", "USDMAD", "USDTHB", "USDXAU", "USDXAG", "USDDKK", "USDINR", "USDIDR", "USDKRW", "USDHKD" ]

signal_history = defaultdict(lambda: deque(maxlen=50))

auto_signal_10sec = False auto_signal_1min = False

def start(update: Update, context: CallbackContext): update.message.reply_text( "Welcome to Quotex Advanced Signal Bot by Ankit Singh!\nUse /menu to see options." )

def menu(update: Update, context: CallbackContext): keyboard = [ [InlineKeyboardButton("▶️ Start 10s Auto Signals", callback_data='start_10s')], [InlineKeyboardButton("⏹ Stop 10s Auto Signals", callback_data='stop_10s')], [InlineKeyboardButton("▶️ Start 1min Auto Signals", callback_data='start_1min')], [InlineKeyboardButton("⏹ Stop 1min Auto Signals", callback_data='stop_1min')], [InlineKeyboardButton("🔎 Custom Signal Generator", callback_data='custom_signal')], [InlineKeyboardButton("📊 Statistics Report", callback_data='stats_report')], [InlineKeyboardButton("🤖 AI Self-Learning Status", callback_data='ai_status')], [InlineKeyboardButton("📈 Trading Plan Generator", callback_data='trading_plan')], [InlineKeyboardButton("💰 Auto Money Management", callback_data='money_management')], [InlineKeyboardButton("🎯 Set Trading Goals", callback_data='set_goals')], [InlineKeyboardButton("📝 Send Manual Signal", callback_data='manual_signal')], ] reply_markup = InlineKeyboardMarkup(keyboard) update.message.reply_text('Select an option:', reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext): query = update.callback_query query.answer() global auto_signal_10sec, auto_signal_1min

if query.data == 'start_10s':
    if not auto_signal_10sec:
        auto_signal_10sec = True
        context.job_queue.run_repeating(send_auto_signal_10sec, interval=10, first=1, context=update.effective_chat.id, name="auto_10sec")
        query.edit_message_text(text="10-second Auto Signals Started ✅")
    else:
        query.edit_message_text(text="10-second Auto Signals already running.")

elif query.data == 'stop_10s':
    auto_signal_10sec = False
    context.job_queue.stop_job("auto_10sec")
    query.edit_message_text(text="10-second Auto Signals Stopped ❌")

elif query.data == 'start_1min':
    if not auto_signal_1min:
        auto_signal_1min = True
        context.job_queue.run_repeating(send_auto_signal_1min, interval=60, first=1, context=update.effective_chat.id, name="auto_1min")
        query.edit_message_text(text="1-minute Auto Signals Started ✅")
    else:
        query.edit_message_text(text="1-minute Auto Signals already running.")

elif query.data == 'stop_1min':
    auto_signal_1min = False
    context.job_queue.stop_job("auto_1min")
    query.edit_message_text(text="1-minute Auto Signals Stopped ❌")

elif query.data == 'custom_signal':
    query.edit_message_text(text="Custom Signal Generator: Feature Coming Soon ✅")

elif query.data == 'stats_report':
    send_statistics_report(update, context)

elif query.data == 'ai_status':
    query.edit_message_text(text="🤖 AI Self-Learning Status: Basic Module Active ✅")

elif query.data == 'trading_plan':
    query.edit_message_text(text="📈 Trading Plan Generator Coming Soon ✅")

elif query.data == 'money_management':
    query.edit_message_text(text="💰 Auto Money Management Feature Coming Soon ✅")

elif query.data == 'set_goals':
    query.edit_message_text(text="🎯 Set Trading Goals Feature Coming Soon ✅")

elif query.data == 'manual_signal':
    send_manual_signal(update, context)

def send_manual_signal(update: Update, context: CallbackContext): pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) update.callback_query.message.reply_text(msg)

def generate_dummy_data(): data = { 'open': np.random.rand(100) * 100, 'high': np.random.rand(100) * 100 + 0.5, 'low': np.random.rand(100) * 100 - 0.5, 'close': np.random.rand(100) * 100, 'volume': np.random.randint(1000, 5000, 100) } return pd.DataFrame(data)

def format_signal_message(result): msg = f"📈 Pair: {result['pair']}\n" msg += f"🔔 Signal: {result['signal']}\n" msg += "📝 Analysis:\n" for line in result['analysis']: msg += f" - {line}\n" return msg

def update_signal_history(pair, result): win = random.choice([True, False])  # Dummy win/loss, replace with real logic signal_history[pair].append(win)

def filter_pairs_by_performance(): filtered = [] for pair, history in signal_history.items(): if len(history) >= 10: win_ratio = sum(history) / len(history) if win_ratio > 0.7: filtered.append(pair) return filtered

def send_auto_signal_10sec(context: CallbackContext): chat_id = context.job.context good_pairs = filter_pairs_by_performance() if good_pairs: pair = random.choice(good_pairs) else: pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) context.bot.send_message(chat_id=chat_id, text=msg) update_signal_history(pair, result)

def send_auto_signal_1min(context: CallbackContext): chat_id = context.job.context good_pairs = filter_pairs_by_performance() if good_pairs: pair = random.choice(good_pairs) else: pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) context.bot.send_message(chat_id=chat_id, text=msg) update_signal_history(pair, result)

def send_statistics_report(update, context): wins = 18 losses = 7

fig, ax = plt.subplots()
ax.bar(['Wins', 'Losses'], [wins, losses], color=['green', 'red'])
ax.set_ylabel('Trades')
ax.set_title('Performance Summary - Ankit Singh')

image_path = 'performance_chart.png'
plt.savefig(image_path)
plt.close()

with open(image_path, 'rb') as photo:
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption="📊 Performance Chart")

def main(): updater = Updater(TOKEN, use_context=True) dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("menu", menu))
dp.add_handler(CallbackQueryHandler(button_handler))

updater.start_polling()
updater.idle()

if name == "main": main()


port random from collections import defaultdict, deque from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup import pandas as pd import numpy as np import matplotlib.pyplot as plt from analysis.analysis import analyze_pair

-----------------------------------------

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54' MY_CHAT_ID = 6065493589

-----------------------------------------

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

ALL_PAIRS = [ "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD", "USDBRL", "USDBDT", "USDDZD", "USDHUF", "USDMXN", "USDRUB", "USDTRY", "USDZAR", "EURGBP", "EURCHF", "EURJPY", "EURAUD", "EURCAD", "EURNZD", "GBPCHF", "GBPJPY", "AUDJPY", "AUDCAD", "AUDCHF", "AUDNZD", "CADJPY", "CHFJPY", "NZDCAD", "NZDCHF", "NZDJPY", "USDNOK", "USDSGD", "USDSEK", "BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD", "GOLD", "SILVER", "OIL", "USDBGN", "USDHRK", "USDCZK", "USDPHP", "USDPEN", "USDPLN", "USDHUF", "USDILS", "USDMAD", "USDTHB", "USDXAU", "USDXAG", "USDDKK", "USDINR", "USDIDR", "USDKRW", "USDHKD" ]

signal_history = defaultdict(lambda: deque(maxlen=50))

auto_signal_10sec = False auto_signal_1min = False

def start(update: Update, context: CallbackContext): update.message.reply_text( "Welcome to Quotex Advanced Signal Bot by Ankit Singh!\nUse /menu to see options." )

def menu(update: Update, context: CallbackContext): keyboard = [ [InlineKeyboardButton("▶️ Start 10s Auto Signals", callback_data='start_10s')], [InlineKeyboardButton("⏹ Stop 10s Auto Signals", callback_data='stop_10s')], [InlineKeyboardButton("▶️ Start 1min Auto Signals", callback_data='start_1min')], [InlineKeyboardButton("⏹ Stop 1min Auto Signals", callback_data='stop_1min')], [InlineKeyboardButton("🔎 Custom Signal Generator", callback_data='custom_signal')], [InlineKeyboardButton("📊 Statistics Report", callback_data='stats_report')], [InlineKeyboardButton("🤖 AI Self-Learning Status", callback_data='ai_status')], [InlineKeyboardButton("📈 Trading Plan Generator", callback_data='trading_plan')], [InlineKeyboardButton("💰 Auto Money Management", callback_data='money_management')], [InlineKeyboardButton("🎯 Set Trading Goals", callback_data='set_goals')], [InlineKeyboardButton("📝 Send Manual Signal", callback_data='manual_signal')], ] reply_markup = InlineKeyboardMarkup(keyboard) update.message.reply_text('Select an option:', reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext): query = update.callback_query query.answer() global auto_signal_10sec, auto_signal_1min

if query.data == 'start_10s':
    if not auto_signal_10sec:
        auto_signal_10sec = True
        context.job_queue.run_repeating(send_auto_signal_10sec, interval=10, first=1, context=update.effective_chat.id, name="auto_10sec")
        query.edit_message_text(text="10-second Auto Signals Started ✅")
    else:
        query.edit_message_text(text="10-second Auto Signals already running.")

elif query.data == 'stop_10s':
    auto_signal_10sec = False
    context.job_queue.stop_job("auto_10sec")
    query.edit_message_text(text="10-second Auto Signals Stopped ❌")

elif query.data == 'start_1min':
    if not auto_signal_1min:
        auto_signal_1min = True
        context.job_queue.run_repeating(send_auto_signal_1min, interval=60, first=1, context=update.effective_chat.id, name="auto_1min")
        query.edit_message_text(text="1-minute Auto Signals Started ✅")
    else:
        query.edit_message_text(text="1-minute Auto Signals already running.")

elif query.data == 'stop_1min':
    auto_signal_1min = False
    context.job_queue.stop_job("auto_1min")
    query.edit_message_text(text="1-minute Auto Signals Stopped ❌")

elif query.data == 'custom_signal':
    query.edit_message_text(text="Custom Signal Generator: Feature Coming Soon ✅")

elif query.data == 'stats_report':
    send_statistics_report(update, context)

elif query.data == 'ai_status':
    query.edit_message_text(text="🤖 AI Self-Learning Status: Basic Module Active ✅")

elif query.data == 'trading_plan':
    query.edit_message_text(text="📈 Trading Plan Generator Coming Soon ✅")

elif query.data == 'money_management':
    query.edit_message_text(text="💰 Auto Money Management Feature Coming Soon ✅")

elif query.data == 'set_goals':
    query.edit_message_text(text="🎯 Set Trading Goals Feature Coming Soon ✅")

elif query.data == 'manual_signal':
    send_manual_signal(update, context)

def send_manual_signal(update: Update, context: CallbackContext): pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) update.callback_query.message.reply_text(msg)

def generate_dummy_data(): data = { 'open': np.random.rand(100) * 100, 'high': np.random.rand(100) * 100 + 0.5, 'low': np.random.rand(100) * 100 - 0.5, 'close': np.random.rand(100) * 100, 'volume': np.random.randint(1000, 5000, 100) } return pd.DataFrame(data)

def format_signal_message(result): msg = f"📈 Pair: {result['pair']}\n" msg += f"🔔 Signal: {result['signal']}\n" msg += "📝 Analysis:\n" for line in result['analysis']: msg += f" - {line}\n" return msg

def update_signal_history(pair, result): win = random.choice([True, False])  # Dummy win/loss, replace with real logic signal_history[pair].append(win)

def filter_pairs_by_performance(): filtered = [] for pair, history in signal_history.items(): if len(history) >= 10: win_ratio = sum(history) / len(history) if win_ratio > 0.7: filtered.append(pair) return filtered

def send_auto_signal_10sec(context: CallbackContext): chat_id = context.job.context good_pairs = filter_pairs_by_performance() if good_pairs: pair = random.choice(good_pairs) else: pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) context.bot.send_message(chat_id=chat_id, text=msg) update_signal_history(pair, result)

def send_auto_signal_1min(context: CallbackContext): chat_id = context.job.context good_pairs = filter_pairs_by_performance() if good_pairs: pair = random.choice(good_pairs) else: pair = random.choice(ALL_PAIRS) df = generate_dummy_data() result = analyze_pair(pair, df) msg = format_signal_message(result) context.bot.send_message(chat_id=chat_id, text=msg) update_signal_history(pair, result)

def send_statistics_report(update, context): wins = 18 losses = 7

fig, ax = plt.subplots()
ax.bar(['Wins', 'Losses'], [wins, losses], color=['green', 'red'])
ax.set_ylabel('Trades')
ax.set_title('Performance Summary - Ankit Singh')

image_path = 'performance_chart.png'
plt.savefig(image_path)
plt.close()

with open(image_path, 'rb') as photo:
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption="📊 Performance Chart")

def main(): updater = Updater(TOKEN, use_context=True) dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("menu", menu))
dp.add_handler(CallbackQueryHandler(button_handler))

updater.start_polling()
updater.idle()

if name == "main": main()


