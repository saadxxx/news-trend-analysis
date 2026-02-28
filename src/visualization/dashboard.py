"""
交互式仪表板，用于可视化新闻趋势。
Interactive dashboard for visualizing news trends.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from analysis.trend_calculator import load_trend_data

st.set_page_config(page_title="News Trend Dashboard", layout="wide")
st.title("📈 News Trend Analysis Pipeline")

# 加载数据
@st.cache_data
def load_data():
    return load_trend_data()  # 假设有函数加载预处理结果

df = load_data()
if df is not None:
    # 主题选择器
    topics = df['topic'].unique()
    selected_topic = st.selectbox("Select a Topic", topics)
    
    # 过滤数据
    topic_df = df[df['topic'] == selected_topic]
    
    # 绘制趋势图
    fig = px.line(topic_df, x='date', y='prevalence', title=f"Trend for Topic: {selected_topic}")
    st.plotly_chart(fig, use_container_width=True)
    
    # 情感分析展示
    fig2 = px.bar(topic_df, x='date', y='sentiment', color='sentiment', title="Sentiment Over Time")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No data available. Please run the pipeline first.")
