import sys
sys.path.append('.')

from src.visualization.plot_generator import VisualizationGenerator

viz = VisualizationGenerator()

print("1. 生成词云图...")
try:
    word_freq = {'AI': 150, '人工智能': 120, '机器学习': 100}
    result1 = viz.generate_wordcloud(word_freq)
    print(f"   成功: {result1}")
except Exception as e:
    print(f"   失败: {e}")

print("\n2. 生成热力图...")
try:
    import pandas as pd
    import numpy as np
    dates = pd.date_range('2024-01-01', periods=10, freq='D')
    topic_trends = pd.DataFrame(
        np.random.rand(10, 5),
        index=dates,
        columns=[f'Topic_{i}' for i in range(5)]
    )
    result2 = viz.generate_trend_heatmap(topic_trends)
    print(f"   成功: {result2}")
except Exception as e:
    print(f"   失败: {e}")

print("\n3. 生成情感时间线...")
try:
    sentiment_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=10, freq='D'),
        'sentiment_score': np.random.uniform(-1, 1, 10),
        'article_count': np.random.randint(50, 200, 10)
    })
    result3 = viz.generate_sentiment_timeline(sentiment_data)
    print(f"   成功: {result3}")
except Exception as e:
    print(f"   失败: {e}")

print("\n4. 生成话题分布...")
try:
    topic_data = pd.DataFrame({
        'topic_name': [f'Topic_{i}' for i in range(5)],
        'article_count': np.random.randint(100, 500, 5),
        'avg_sentiment': np.random.uniform(-0.5, 0.5, 5)
    })
    result4 = viz.generate_topic_distribution(topic_data)
    print(f"   成功: {result4}")
except Exception as e:
    print(f"   失败: {e}")

print("\n5. 检查依赖...")
try:
    import plotly
    import matplotlib
    print(f"   Plotly版本: {plotly.__version__}")
    print(f"   Matplotlib版本: {matplotlib.__version__}")
except Exception as e:
    print(f"   检查失败: {e}")
