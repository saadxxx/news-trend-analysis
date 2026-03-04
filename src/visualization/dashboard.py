"""
Streamlit News Trend Analysis Dashboard - Main Application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path
import sys
from typing import Optional
import numpy as np
import os
import logging
from src.visualization.plot_generator import VisualizationGenerator


# 定义 setup_logger 函数（添加到 dashboard.py 开头）
def setup_logger(name, log_level=logging.INFO):
    """
    创建并配置一个标准化的 logger 实例
    :param name: logger 名称
    :param log_level: 日志级别（默认 INFO）
    :return: 配置好的 logger 对象
    """
    # 创建 logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 定义日志格式
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 1. 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # 2. 文件处理器（可选，日志保存到文件）
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    return logger

# 原有代码（第40行）
logger = setup_logger("dashboard")

# 定义 generate_demo_results 函数
def generate_demo_results():
    """
    生成演示用的可视化结果（适配你的新闻趋势分析项目）
    功能：创建示例数据 → 调用可视化生成器 → 生成并保存各类图表
    """
    logger.info("开始生成演示可视化结果...")  # 使用之前配置的logger
    
    # 确保输出目录存在
    output_dir = "docs/images"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建可视化生成器实例
    viz = VisualizationGenerator()
    
    try:
        # 1. 生成示例词频数据（词云用）
        word_freq = {
            'AI': 150, '人工智能': 120, '机器学习': 100,
            '大数据': 80, '深度学习': 70, '自然语言处理': 60
        }
        wordcloud_path = viz.generate_wordcloud(word_freq, title="News Topic Word Cloud")
        logger.info(f"词云图生成完成：{wordcloud_path}")
        
        # 2. 生成示例趋势数据（热力图用）
        dates = pd.date_range('2024-01-01', periods=10, freq='D')
        topic_trends = pd.DataFrame(
            np.random.rand(10, 5),
            index=dates,
            columns=[f'Topic_{i}' for i in range(5)]
        )
        heatmap_path = viz.generate_trend_heatmap(topic_trends)
        logger.info(f"趋势热力图生成完成：{heatmap_path}")
        
        # 3. 生成示例情感数据（时间线用）
        sentiment_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10, freq='D'),
            'sentiment_score': np.random.uniform(-1, 1, 10),
            'article_count': np.random.randint(50, 200, 10)
        })
        timeline_path = viz.generate_sentiment_timeline(sentiment_data)
        logger.info(f"情感时间线生成完成：{timeline_path}")
        
        # 4. 生成示例话题数据（分布图表用）
        topic_data = pd.DataFrame({
            'topic_name': [f'Topic_{i}' for i in range(5)],
            'article_count': np.random.randint(100, 500, 5),
            'avg_sentiment': np.random.uniform(-0.5, 0.5, 5)
        })
        distribution_path = viz.generate_topic_distribution(topic_data)
        logger.info(f"话题分布图生成完成：{distribution_path}")
        
        logger.info("所有演示可视化结果生成完成！")
        return {
            "wordcloud": wordcloud_path,
            "heatmap": heatmap_path,
            "timeline": timeline_path,
            "distribution": distribution_path
        }
    
    except Exception as e:
        logger.error(f"生成演示结果失败：{str(e)}", exc_info=True)
        raise  # 抛出异常，方便排查问题

# 原有代码第682行
generate_demo_results()

if os.name == 'nt':  # Windows
    # Force UTF-8 encoding
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
# Add project root directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Set page configuration (must be at the beginning)
st.set_page_config(
    page_title="News Trend Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import project modules
try:
    from src.utils.logger import setup_logger
    from src.visualization.plot_generator import VisualizationGenerator
except ImportError as e:
    st.warning(f"Some modules failed to import: {e}")
    st.info("Suggested to run in project root directory: `pip install -r requirements.txt`")

# Initialize logger
logger = setup_logger("dashboard")

# Application title and introduction
st.title("📈 News Trend Analysis and Topic Modeling Dashboard")
st.markdown("""
<div style="background-color:#f0f2f6;padding:20px;border-radius:10px;margin-bottom:20px;">
<h4 style="color:#1f77b4;margin-top:0;">Welcome to News Trend Analysis System</h4>
<p>This dashboard provides real-time news data topic identification, sentiment analysis, and trend tracking.</p>
<ul>
<li><strong>Topic Modeling</strong>: Automatically identify core topics in news</li>
<li><strong>Sentiment Analysis</strong>: Analyze emotional tendencies in news reports</li>
<li><strong>Trend Tracking</strong>: Visualize topic popularity changes over time</li>
<li><strong>Interactive Exploration</strong>: Click charts to get detailed information</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    # Data source selection
    data_source = st.selectbox(
        "Select Data Source",
        ["Sample Data", "Real-time Data", "Custom Upload"],
        help="Select data source for analysis"
    )
    
    # Time range selection
    st.subheader("📅 Time Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30),
            max_value=datetime.now()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            min_value=start_date,
            max_value=datetime.now()
        )
    
    # Topic count selection
    topic_count = st.slider(
        "Display Topic Count",
        min_value=3,
        max_value=20,
        value=8,
        help="Control number of main topics to display"
    )
    
    # Sentiment threshold setting
    st.subheader("🎭 Sentiment Analysis Settings")
    sentiment_threshold = st.slider(
        "Sentiment Intensity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Filter out data with sentiment intensity below this value"
    )
    
    # Analysis button
    st.markdown("---")
    analyze_button = st.button(
        "🚀 Start Analysis",
        type="primary",
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("""
    ### 📊 Quick Actions
    - 📥 Import New Data
    - 💾 Save Current View
    - 📤 Export Analysis Report
    - 🔄 Refresh Data
    """)
    
    # System status
    st.markdown("---")
    st.caption("**System Status**")
    st.progress(75, text="Data Loading: 75%")
    st.caption(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Topic Analysis", "📈 Trend Tracking", "📄 Detailed Report"])

with tab1:
    st.header("Data Overview")
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Articles",
            value="1,254",
            delta="+42 (Today)",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Identified Topics",
            value="8",
            delta="-2 (Yesterday)",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Average Sentiment",
            value="+0.15",
            delta="+0.03",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Data Coverage",
            value="85%",
            delta="+5%",
            delta_color="normal"
        )
    
    # Topic distribution and sentiment trend
    st.subheader("Topic Distribution and Sentiment Trend")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Topic distribution pie chart
        topic_data = {
            "Topic": ["AI Regulation", "Climate Policy", "Chip Competition", "Economic Recovery", "Medical Breakthrough", "EdTech", "Cybersecurity", "Others"],
            "Article Count": [320, 280, 240, 200, 160, 120, 80, 100]
        }
        df_topics = pd.DataFrame(topic_data)
        
        fig1 = px.pie(
            df_topics,
            values='Article Count',
            names='Topic',
            title='Topic Distribution',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Sentiment trend chart
        dates = pd.date_range(start_date, end_date, freq='D')
        sentiment_data = {
            "Date": dates,
            "Sentiment Score": 0.3 + 0.4 * (pd.Series(range(len(dates))) / len(dates)) + 0.1 * np.random.randn(len(dates)),
            "Article Count": np.random.randint(30, 100, len(dates))
        }
        df_sentiment = pd.DataFrame(sentiment_data)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_sentiment["Date"],
            y=df_sentiment["Sentiment Score"],
            mode='lines',
            name='Sentiment Score',
            line=dict(color='royalblue', width=3),
            fill='tozeroy',
            fillcolor='rgba(65, 105, 225, 0.1)'
        ))
        
        fig2.update_layout(
            title='Sentiment Trend',
            xaxis_title='Date',
            yaxis_title='Sentiment Score',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Real-time data preview
    st.subheader("📰 Real-time News Preview")
    
    sample_articles = [
        {
            "Title": "EU Passes New AI Regulation Bill",
            "Source": "Reuters",
            "Time": "2 hours ago",
            "Sentiment": "Positive",
            "Topic": "AI Regulation"
        },
        {
            "Title": "Global Chip Supply Shortage Eases",
            "Source": "Wall Street Journal",
            "Time": "5 hours ago",
            "Sentiment": "Neutral",
            "Topic": "Chip Competition"
        },
        {
            "Title": "Historic Emission Reduction Agreement Reached at Climate Summit",
            "Source": "BBC",
            "Time": "1 day ago",
            "Sentiment": "Positive",
            "Topic": "Climate Policy"
        },
        {
            "Title": "Tech Giants Release Quarterly Earnings Reports",
            "Source": "CNN",
            "Time": "2 days ago",
            "Sentiment": "Mixed",
            "Topic": "Economic Recovery"
        }
    ]
    
    for article in sample_articles:
        with st.expander(f"{article['Title']} ({article['Source']})"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sentiment", article['Sentiment'])
            with col2:
                st.metric("Topic", article['Topic'])
            with col3:
                st.metric("Time", article['Time'])
            
            if st.button(f"Analyze Full Text", key=f"btn_{article['Title'][:10]}"):
                st.info(f"Analyzing article: {article['Title']}")
                st.success("Analysis complete! Key entities: AI, Regulation, Policy")

with tab2:
    st.header("Topic Detailed Analysis")
    
    # Topic selector
    selected_topic = st.selectbox(
        "Select topic to analyze",
        ["AI Regulation & Ethics", "Climate Change Policy", "Global Chip Competition", "Economic Recovery", "Medical Tech Innovation", "Digital Education Transformation", "Cybersecurity Challenges"],
        index=0
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Topic heat trend
        st.subheader(f"Topic Heat Trend: {selected_topic}")
        
        # Generate sample trend data
        days = 30
        dates = [start_date + timedelta(days=i) for i in range(days)]
        base_trend = np.linspace(0.3, 0.8, days)
        noise = np.random.normal(0, 0.1, days)
        heat_scores = np.clip(base_trend + noise, 0, 1)
        
        trend_df = pd.DataFrame({
            "Date": dates,
            "Heat Score": heat_scores,
            "Article Count": np.random.randint(10, 50, days)
        })
        
        fig_trend = px.line(
            trend_df,
            x="Date",
            y="Heat Score",
            title=f"{selected_topic} Heat Trend",
            markers=True
        )
        
        # Add article count bar chart
        fig_trend.add_trace(go.Bar(
            x=trend_df["Date"],
            y=trend_df["Article Count"],
            name="Article Count",
            yaxis="y2",
            opacity=0.3
        ))
        
        fig_trend.update_layout(
            yaxis2=dict(
                title="Article Count",
                overlaying="y",
                side="right"
            ),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # Topic statistics
        st.subheader("Topic Statistics")
        
        stats_data = {
            "Metric": ["Total Articles", "Average Sentiment", "Peak Heat", "Duration", "Related Topics", "Media Coverage"],
            "Value": ["320 articles", "+0.25", "0.89", "15 days", "3 topics", "87%"]
        }
        
        st.dataframe(
            pd.DataFrame(stats_data),
            use_container_width=True,
            hide_index=True
        )
        
        # Topic keywords
        st.subheader("🔑 Keyword Cloud")
        
        if selected_topic == "AI Regulation & Ethics":
            keywords = ["AI", "Regulation", "Ethics", "Algorithm", "Transparency", "Responsibility", "Policy", "Bill", "Compliance", "Governance"]
        elif selected_topic == "Climate Change Policy":
            keywords = ["Climate", "Environment", "Emission Reduction", "Energy", "Sustainable", "Carbon", "Green", "Policy", "Agreement", "Ecology"]
        else:
            keywords = ["Technology", "Innovation", "Development", "Market", "Competition", "Investment", "Strategy", "Future", "Challenge", "Opportunity"]
        
        # Create keyword display
        keyword_html = "<div style='line-height:2.5;'>"
        for kw in keywords:
            size = np.random.randint(14, 24)
            color = f"hsl({np.random.randint(0, 360)}, 70%, 60%)"
            keyword_html += f"<span style='font-size:{size}px; color:{color}; margin:5px; padding:5px 10px; background:#f0f0f0; border-radius:15px; display:inline-block;'>{kw}</span>"
        keyword_html += "</div>"
        
        st.markdown(keyword_html, unsafe_allow_html=True)
    
    # Related articles list
    st.subheader("📄 Related Articles")
    
    related_articles = [
        {"title": f"Latest Research Progress on {selected_topic}", "source": "Science Daily", "date": "2024-01-15", "sentiment": 0.6},
        {"title": f"Expert Interpretation of {selected_topic} Future Trends", "source": "Tech Review", "date": "2024-01-12", "sentiment": 0.4},
        {"title": f"Policy Makers Discuss {selected_topic} Implementation Plan", "source": "Policy Journal", "date": "2024-01-10", "sentiment": 0.2},
        {"title": f"How Enterprises Respond to Challenges Brought by {selected_topic}", "source": "Business Weekly", "date": "2024-01-08", "sentiment": 0.3},
    ]
    
    for i, article in enumerate(related_articles):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{article['title']}**")
                st.caption(f"Source: {article['source']} | Date: {article['date']}")
            with col2:
                sentiment_color = "green" if article['sentiment'] > 0 else "red" if article['sentiment'] < 0 else "gray"
                st.markdown(f"<span style='color:{sentiment_color};'>Sentiment: {article['sentiment']:+.2f}</span>", unsafe_allow_html=True)
            with col3:
                if st.button("View Details", key=f"detail_{i}"):
                    st.session_state[f"show_detail_{i}"] = not st.session_state.get(f"show_detail_{i}", False)
            
            if st.session_state.get(f"show_detail_{i}", False):
                st.info(f"This is a detailed analysis article about {selected_topic}, discussing current hot issues and future development directions.")
            st.divider()

with tab3:
    st.header("Trend Tracking and Prediction")
    
    # Multi-topic comparison
    st.subheader("Multi-topic Heat Comparison")
    
    topics_comparison = ["AI Regulation", "Climate Policy", "Chip Competition", "Economic Recovery", "Medical Breakthrough"]
    comparison_data = []
    
    for topic in topics_comparison:
        base = np.random.uniform(0.3, 0.7)
        trend = np.random.uniform(-0.2, 0.2)
        days = 30
        values = [base + trend * (i/days) + np.random.normal(0, 0.05) for i in range(days)]
        values = np.clip(values, 0, 1)
        
        for i, val in enumerate(values):
            comparison_data.append({
                "Date": start_date + timedelta(days=i),
                "Heat": val,
                "Topic": topic
            })
    
    df_comparison = pd.DataFrame(comparison_data)
    
    fig_comparison = px.line(
        df_comparison,
        x="Date",
        y="Heat",
        color="Topic",
        title="Multi-topic Heat Comparison",
        line_shape="spline"
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Prediction analysis
    st.subheader("📈 Trend Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Next 7 Days Prediction
        - **AI Regulation**: ↗ Rising Trend (Confidence: 85%)
        - **Climate Policy**: → Stable (Confidence: 75%)
        - **Chip Competition**: ↘ Declining Trend (Confidence: 70%)
        - **Economic Recovery**: ↗ Slowly Rising (Confidence: 65%)
        """)
    
    with col2:
        # Prediction chart
        future_dates = [end_date + timedelta(days=i) for i in range(1, 8)]
        predictions = {
            "AI Regulation": [0.7, 0.72, 0.75, 0.77, 0.78, 0.79, 0.8],
            "Climate Policy": [0.6, 0.61, 0.61, 0.62, 0.62, 0.63, 0.63],
            "Chip Competition": [0.5, 0.49, 0.48, 0.47, 0.46, 0.45, 0.44]
        }
        
        fig_predict = go.Figure()
        for topic, values in predictions.items():
            fig_predict.add_trace(go.Scatter(
                x=future_dates,
                y=values,
                name=topic,
                mode='lines+markers',
                line=dict(dash='dash')
            ))
        
        fig_predict.update_layout(
            title="Topic Heat Prediction",
            xaxis_title="Date",
            yaxis_title="Predicted Heat",
            template="plotly_white"
        )
        
        st.plotly_chart(fig_predict, use_container_width=True)

with tab4:
    st.header("Analysis Report")
    
    # Report generation options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["Daily Report", "Weekly Report", "Monthly Report", "Special Report"]
        )
    
    with col2:
        report_format = st.selectbox(
            "Export Format",
            ["HTML", "PDF", "Markdown", "Word"]
        )
    
    with col3:
        include_charts = st.checkbox("Include Charts", value=True)
        include_data = st.checkbox("Include Raw Data", value=False)
    
    # Generate report button
    if st.button("📄 Generate Analysis Report", type="primary", use_container_width=True):
        with st.spinner("Generating report..."):
            # Simulate report generation process
            import time
            time.sleep(2)
            
            # Display report preview
            st.success("Report generated successfully!")
            
            # Report content
            st.subheader("Report Preview")
            
            report_content = f"""
            # News Trend Analysis Report
            **Report Type**: {report_type}
            **Generation Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            **Analysis Period**: {start_date} to {end_date}
            
            ## Executive Summary
            During the analysis period, the system processed 1,254 news articles and identified 8 core topics. The overall sentiment tendency is slightly positive (+0.15).
            
            ## Key Findings
            1. **AI regulation topic heat continues to rise**, with 45% growth after EU bill passage
            2. **Climate policy topic has the most positive sentiment**, average sentiment score reaches +0.60
            3. **Chip competition topic shows regional differences**, different reporting angles across regions
            
            ## Detailed Analysis
            ### 1. Topic Distribution
            - AI Regulation & Ethics: 320 articles (25.5%)
            - Climate Change Policy: 280 articles (22.3%)
            - Global Chip Competition: 240 articles (19.1%)
            - Other topics: 414 articles (33.0%)
            
            ### 2. Sentiment Analysis
            - Overall average sentiment: +0.15
            - Positive article proportion: 42%
            - Negative article proportion: 28%
            - Neutral article proportion: 30%
            
            ### 3. Trend Prediction
            It is expected that AI regulation topic heat will continue to rise in the next week, while chip competition topic may cool down.
            
            ## Recommendations
            1. Continue to monitor follow-up developments of AI regulation policies
            2. Strengthen research on investment opportunities related to climate policies
            3. Monitor the impact of chip supply chain changes on the industry
            
            ---
            *This report is automatically generated by the News Trend Analysis System*
            """
            
            st.markdown(report_content)
            
            # Export options
            st.download_button(
                label="📥 Download Report",
                data=report_content,
                file_name=f"news_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption("© 2024 News Trend Analysis System")
with footer_col2:
    st.caption("Version: v1.0.0")
with footer_col3:
    st.caption("[View Source Code](https://github.com/yourusername/news-trend-analysis)")

# Add some styles
st.markdown("""
<style>
    /* Main title style */
    .stTitle {
        color: #1f77b4;
    }
    
    /* Sidebar style */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button style */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    
    /* Metric card style */
    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Tab active state */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.analysis_results = None

# Run analysis
if analyze_button:
    with st.spinner("Analyzing data..."):
        import time
        progress_bar = st.progress(0)
        
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        
        st.session_state.data_loaded = True
        st.session_state.analysis_results = {
            "topics": ["AI Regulation", "Climate Policy", "Chip Competition"],
            "sentiment": 0.15,
            "articles_analyzed": 1254
        }
        
        st.success("Analysis complete!")
        st.rerun()

if __name__ == "__main__":
    # In development environment, Streamlit automatically runs this script
    # Development-specific code can be added here
    generate_demo_results()
       
