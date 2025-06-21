import time import logging from collections import deque, defaultdict from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, JobQueue import pandas as pd import numpy as np import ta import random

TOKEN = '7413469925:AAHd7Hi2g3609KoT15MSdrJSeqF1-YlCC54' CHAT_ID = 6065493589

logging.basicConfig(level=logging.INFO)

VOLUME_THRESHOLD = 1000

class BasicAISelfLearning: def init(self, lookback=50, win_threshold=0.7, skip_duration=300): self.lookback = lookback self.win_threshold = win_threshold self.skip_duration = skip_duration self.trade_history = defaultdict(lambda: deque(maxlen=self.lookback)) self.skip_until = {}

def record_trade(self, pair, is_win):
    self.trade_history[pair].append(is_win)
    if pair in self.skip_until and time.time() > self.skip_until[pair]:
        del self.skip_until[pair]

def get_win_ratio(self, pair):
    history = self.trade_history.get(pair, [])
    return sum(history) / len(history) if history else 0.0

def should_skip(self, pair):
    if pair in self.skip_until and time.time() < self.skip_until[pair]:
        return True
    if len(self.trade_history[pair]) == self.lookback and self.get_win_ratio(pair) < self.win_threshold:
        self.skip_until[pair] = time.time() + self.skip_duration
        return True
    return False

def get_priority_pairs(self):
    prioritized = []
    for pair in self.trade_history:
        if not self.should_skip(pair):
            ratio = self.get_win_ratio(pair)
            if ratio >= self.win_threshold:
                prioritized.append((pair, ratio))
    prioritized.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in prioritized]

ai_module = BasicAISelfLearning()

REAL_PAIRS = [ 'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'EURJPY', 'GBPJPY', 'NZDUSD', 'EURGBP', 'USDCAD', 'USDCHF', 'AUDJPY', 'CADJPY', 'CHFJPY', 'AUDNZD', 'EURNZD', 'GBPNZD', 'BTCUSD', 'ETHUSD', 'LTCUSD', 'XRPUSD', 'BNBUSD', 'DOGEUSD', 'SOLUSD', 'ADAUSD', 'GOLD', 'SILVER', 'BRENT', 'PLATINUM' ]

OTC_PAIRS = [ 'EURUSD-OTC', 'GBPUSD-OTC', 'USDJPY-OTC', 'AUDUSD-OTC', 'EURJPY-OTC', 'GBPJPY-OTC', 'NZDUSD-OTC', 'EURGBP-OTC', 'USDCAD-OTC', 'USDCHF-OTC', 'AUDJPY-OTC', 'CADJPY-OTC', 'CHFJPY-OTC', 'AUDNZD-OTC', 'EURNZD-OTC', 'GBPNZD-OTC', 'BTCUSD-OTC', 'ETHUSD-OTC', 'LTCUSD-OTC', 'XRPUSD-OTC', 'BNBUSD-OTC', 'DOGEUSD-OTC', 'SOLUSD-OTC', 'ADAUSD-OTC', 'GOLD-OTC', 'SILVER-OTC', 'BRENT-OTC', 'PLATINUM-OTC', 'APPLE-OTC', 'GOOGLE-OTC', 'AMAZON-OTC', 'TESLA-OTC', 'META-OTC', 'MICROSOFT-OTC', 'ALIBABA-OTC', 'NVIDIA-OTC', 'VISA-OTC', 'JPMORGAN-OTC' ]

EXOTIC_OTC_PAIRS = [ 'USD/BRL-OTC', 'USD/BDT-OTC', 'USD/DZD-OTC', 'USD/INR-OTC', 'USD/NGN-OTC', 'USD/PKR-OTC', 'USD/KZT-OTC', 'USD/EGP-OTC', 'USD/TND-OTC', 'USD/MAD-OTC' ]

ALL_PAIRS = REAL_PAIRS + OTC_PAIRS + EXOTIC_OTC_PAIRS

def generate_signal(pair): return random.choice(['UP', 'DOWN'])

def trade_result(pair, signal): return random.choice(['WIN ✅', 'LOSS ❌'])

def generate_10second_signal(pair, df): df['sma100'] = ta.trend.sma_indicator(df['close'], window=100) df['wma25'] = ta.trend.wma_indicator(df['close'], window=25) df['sma10'] = ta.trend.sma_indicator(df['close'], window=10) df['rsi14'] = ta.momentum.rsi(df['close'], window=14) df['demarker'] = ta.momentum.demarker(df['high'], df['low'], window=14) df['weis_wave'] = df['volume'].rolling(window=5).sum()

last = df.iloc[-1]
candle_range = last['high'] - last['low']
avg_range = (df['high'] - df['low']).rolling(window=20).mean().iloc[-1]

if candle_range < 0.5 * avg_range:
    return {'pair': pair, 'signal': None, 'reason': 'Sideways market'}

if last['weis_wave'] < VOLUME_THRESHOLD:
    return {'pair': pair, 'signal': None, 'reason': 'Low Volume'}

trend_up = last['close'] > last['sma100']
trend_down = last['close'] < last['sma100']

crossover_up = last['sma10'] > last['wma25']
crossover_down = last['sma10'] < last['wma25']

bullish = trend_up and crossover_up and last['rsi14'] < 70 and last['demarker'] > 0.5
bearish = trend_down and crossover_down and last['rsi14'] > 30 and last['demarker'] < 0.5

if bullish:
    return {'pair': pair, 'signal': 'UP', 'reason': 'Bullish Confirmed'}
if bearish:
    return {'pair': pair, 'signal': 'DOWN', 'reason': 'Bearish Confirmed'}

return {'pair': pair, 'signal': None, 'reason': 'No clear signal'}

is_running = False

Manual Code for Auto Signal Mode

auto_mode = False

def auto_signals(context: CallbackContext): global auto_mode if auto_mode and is_running: pair = random.choice(ALL_PAIRS) if ai_module.should_skip(pair): context.bot.send_message(chat_id=CHAT_ID, text=f"❗ Skipping {pair} temporarily due to bad performance", parse_mode="Markdown") return signal = generate_signal(pair) context.bot.send_message(chat_id=CHAT_ID, text=f"⏱ {pair}\n💹 Signal → {signal}\n👑 By Ankit Singh", parse_mode="Markdown") result = trade_result(pair, signal) ai_module.record_trade(pair, result.startswith('WIN')) context.bot.send_message(chat_id=CHAT_ID, text=f"🎯 Result: {result}", parse_mode="Markdown") context.job_queue.run_once(auto_signals, 60)

def auto_on(update: Update, context: CallbackContext): global auto_mode auto_mode = True context.bot.send_message(chat_id=CHAT_ID, text="✅ Auto Mode Started", parse_mode="Markdown") context.job_queue.run_once(auto_signals, 1)

def auto_off(update: Update, context: CallbackContext): global auto_mode auto_mode = False context.bot.send_message(chat_id=CHAT_ID, text="🛑 Auto Mode Stopped", parse_mode="Markdown")

def main(): updater = Updater(token=TOKEN, use_context=True) dp = updater.dispatcher dp.add_handler(CommandHandler("auto_on", auto_on)) dp.add_handler(CommandHandler("auto_off", auto_off)) updater.start_polling() updater.idle()

if name == "main": main()

