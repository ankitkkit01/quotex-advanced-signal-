import matplotlib.pyplot as plt
import random
import os
from datetime import datetime

def generate_statistics_chart():
    wins = random.randint(20, 50)
    losses = random.randint(5, 15)
    total = wins + losses
    accuracy = round((wins / total) * 100, 2)

    status = "✅ GOOD PERFORMANCE" if accuracy >= 75 else ("⚠️ AVERAGE PERFORMANCE" if accuracy >= 50 else "❌ BAD PERFORMANCE")

    labels = ['Wins', 'Losses']
    values = [wins, losses]
    colors = ['green', 'red']

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color=colors)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, color='black')

    ax.set_title('Daily Trading Performance', fontsize=14)
    ax.set_ylabel('Number of Trades')
    plt.tight_layout()

    os.makedirs('assets', exist_ok=True)
    filename = f"assets/performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename)
    plt.close()

    caption = (
        f"📊 *Performance Review — Ankit Singh*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🏆 Wins: {wins}\n"
        f"❌ Losses: {losses}\n"
        f"🎯 Accuracy: {accuracy}%\n"
        f"━━━━━━━━━━━━━━━\n"
        f"Status: {status}"
    )

    return filename, caption
