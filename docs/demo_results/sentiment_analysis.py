import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load and explore the data
df = pd.read_csv('sentiment_analysis.csv')

print("Dataset shape:", df.shape)
print("\nColumn names:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")
    
print("\nFirst few rows:")
print(df.head())

print("\nBasic statistics:")
print(df.describe())

print("\nData types:")
print(df.dtypes)

# Visualization code
# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Set up the plotting style
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Sentiment Analysis Visualization', fontsize=16)

# Plot 1: Average Sentiment Over Time
axes[0, 0].plot(df['date'], df['avg_sentiment'], marker='o', linewidth=2, markersize=4, color=plt.cm.tab20c(1))
axes[0, 0].set_title('Average Sentiment Over Time')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Average Sentiment')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot 2: Sentiment Ratios Over Time
axes[0, 1].plot(df['date'], df['positive_ratio'], label='Positive', marker='o', linewidth=2, markersize=4, color=plt.cm.tab20c(5))
axes[0, 1].plot(df['date'], df['negative_ratio'], label='Negative', marker='s', linewidth=2, markersize=4, color=plt.cm.tab20c(9))
axes[0, 1].plot(df['date'], df['neutral_ratio'], label='Neutral', marker='^', linewidth=2, markersize=4, color=plt.cm.tab20c(13))
axes[0, 1].set_title('Sentiment Ratios Over Time')
axes[0, 1].set_xlabel('Date')
axes[0, 1].set_ylabel('Ratio')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].tick_params(axis='x', rotation=45)

# Plot 3: Total Articles Over Time
axes[1, 0].bar(df['date'], df['total_articles'], color=plt.cm.tab20c(17), alpha=0.7)
axes[1, 0].set_title('Total Articles Over Time')
axes[1, 0].set_xlabel('Date')
axes[1, 0].set_ylabel('Number of Articles')
axes[1, 0].tick_params(axis='x', rotation=45)
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Plot 4: Sentiment Distribution (Pie Chart)
avg_positive = df['positive_ratio'].mean()
avg_negative = df['negative_ratio'].mean()
avg_neutral = df['neutral_ratio'].mean()

axes[1, 1].pie([avg_positive, avg_negative, avg_neutral], 
               labels=['Positive', 'Negative', 'Neutral'],
               colors=[plt.cm.tab20c(5), plt.cm.tab20c(9), plt.cm.tab20c(13)],
               autopct='%1.1f%%',
               startangle=90)
axes[1, 1].set_title('Average Sentiment Distribution')

# Adjust layout and save
plt.tight_layout()
plt.savefig('sentiment_analysis_visualization.png', dpi=300, bbox_inches='tight')
plt.show()

print("Visualization saved as 'sentiment_analysis_visualization.png'")