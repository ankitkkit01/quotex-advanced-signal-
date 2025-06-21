import matplotlib.pyplot as plt
import numpy as np
import os
import random

def generate_statistics_chart():
    labels = ['Wins', 'Losses']
    values = [random.randint(20, 30), random.randint(5, 15)]
    colors = ['green', 'red']

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values, color=colors)
    ax.set_title('Ankit Singh - Trading Performance')
    ax.set_ylabel('Number of Trades')
    for i, v in enumerate(values):
        ax.text(i, v + 0.5, str(v), ha='center', fontweight='bold')

    chart_path = 'assets/performance_chart.png'
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    plt.savefig(chart_path)
    plt.close()
    return chart_path
