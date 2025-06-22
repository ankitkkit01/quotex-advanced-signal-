# reports/report_generator.py

import matplotlib.pyplot as plt
import numpy as np
import io

def generate_performance_chart(wins, losses, accuracy, username="Ankit Singh"):
    """
    Generates a bar chart of performance and returns as byte stream for Telegram
    """
    labels = ['Wins', 'Losses']
    values = [wins, losses]
    colors = ['green', 'red']

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, values, color=colors)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', fontsize=12, fontweight='bold')

    ax.set_ylabel('Number of Trades', fontsize=12)
    ax.set_title(f'{username} Performance Report\nAccuracy: {accuracy}%', fontsize=14, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf