import time
import random

def report_trade_result(bot, chat_id, asset, direction):
    time.sleep(300)  # 5 minutes = 300 seconds
    result = random.choice(["WIN ✅", "LOSS ❌"])
    bot.send_message(chat_id=chat_id, text=f"""
📊 *Trade Result*

📌 *Asset:* {asset}
📉 *Direction:* {direction}
🏆 *Result:* {result}
""", parse_mode='Markdown')
