import random
from telegram import Bot
import time
from utils.time_utils import get_current_ist_time

def report_trade_result(bot: Bot, chat_id, pair, direction):
    """
    Sends the trade result after a delay (simulating result time).
    """
    time.sleep(300)  # 5 minutes delay (300 seconds)

    # Simulate WIN or LOSS
    result = random.choice(["✅ WIN", "❌ LOSS"])

    # Send Result Message
    bot.send_message(
        chat_id=chat_id,
        text=f"""
🎯 *Trade Result*

📌 *Asset:* {pair}
📉 *Direction:* {direction}
⏰ *Time:* {get_current_ist_time()}

📊 *Result:* {result}
""",
        parse_mode='Markdown'
    )
