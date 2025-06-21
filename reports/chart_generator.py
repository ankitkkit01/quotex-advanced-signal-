import matplotlib.pyplot as plt
import os

class ChartGenerator:
    def __init__(self, output_dir="reports/charts"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_performance_chart(self, wins, losses, filename="performance_chart.png"):
        labels = ['Wins', 'Losses']
        values = [wins, losses]
        colors = ['#4CAF50', '#F44336']

        plt.figure(figsize=(6,4))
        bars = plt.bar(labels, values, color=colors)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=12)
        plt.title('Trading Performance')
        plt.ylabel('Number of Trades')
        plt.ylim(0, max(values) + 5)
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath)
        plt.close()
        print(f"Chart saved at {filepath}")
        return filepath

if __name__ == "__main__":
    gen = ChartGenerator()
    gen.generate_performance_chart(wins=7, losses=3)
