"""
Streamlit新闻趋势分析仪表板 - 主应用
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

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))

# 设置页面配置（必须放在最前面）
st.set_page_config(
    page_title="新闻趋势分析仪表板",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 导入项目模块
try:
    from src.utils.logger import setup_logger
    from src.visualization.plot_generator import VisualizationGenerator
except ImportError as e:
    st.warning(f"某些模块导入失败: {e}")
    st.info("建议在项目根目录运行: `pip install -r requirements.txt`")

# 初始化日志
logger = setup_logger("dashboard")

# 应用标题和介绍
st.title("📈 新闻趋势分析与主题建模仪表板")
st.markdown("""
<div style="background-color:#f0f2f6;padding:20px;border-radius:10px;margin-bottom:20px;">
<h4 style="color:#1f77b4;margin-top:0;">欢迎使用新闻趋势分析系统</h4>
<p>本仪表板提供实时新闻数据的话题识别、情感分析和趋势追踪功能。</p>
<ul>
<li><strong>话题建模</strong>: 自动识别新闻中的核心话题</li>
<li><strong>情感分析</strong>: 分析新闻报道的情感倾向</li>
<li><strong>趋势追踪</strong>: 可视化话题热度随时间变化</li>
<li><strong>交互探索</strong>: 点击图表获取详细信息</li>
</ul>
</div>
""", unsafe_allow_html=True)

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 控制面板")
    
    # 数据源选择
    data_source = st.selectbox(
        "选择数据源",
        ["示例数据", "实时数据", "自定义上传"],
        help="选择要分析的数据来源"
    )
    
    # 时间范围选择
    st.subheader("📅 时间范围")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "开始日期",
            value=datetime.now() - timedelta(days=30),
            max_value=datetime.now()
        )
    with col2:
        end_date = st.date_input(
            "结束日期",
            value=datetime.now(),
            min_value=start_date,
            max_value=datetime.now()
        )
    
    # 话题数量选择
    topic_count = st.slider(
        "显示话题数量",
        min_value=3,
        max_value=20,
        value=8,
        help="控制显示的主要话题数量"
    )
    
    # 情感阈值设置
    st.subheader("🎭 情感分析设置")
    sentiment_threshold = st.slider(
        "情感强度阈值",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="过滤掉情感强度低于此值的数据"
    )
    
    # 分析按钮
    st.markdown("---")
    analyze_button = st.button(
        "🚀 开始分析",
        type="primary",
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("""
    ### 📊 快速操作
    - 📥 导入新数据
    - 💾 保存当前视图
    - 📤 导出分析报告
    - 🔄 刷新数据
    """)
    
    # 系统状态
    st.markdown("---")
    st.caption("**系统状态**")
    st.progress(75, text="数据加载: 75%")
    st.caption(f"最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 主内容区域
tab1, tab2, tab3, tab4 = st.tabs(["📊 概览", "🎯 话题分析", "📈 趋势追踪", "📄 详细报告"])

with tab1:
    st.header("数据概览")
    
    # 创建指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="总文章数",
            value="1,254",
            delta="+42 (今日)",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="识别话题数",
            value="8",
            delta="-2 (昨日)",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="平均情感",
            value="+0.15",
            delta="+0.03",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="数据覆盖率",
            value="85%",
            delta="+5%",
            delta_color="normal"
        )
    
    # 话题分布和情感趋势
    st.subheader("话题分布与情感趋势")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 话题分布饼图
        topic_data = {
            "话题": ["AI监管", "气候政策", "芯片竞争", "经济复苏", "医疗突破", "教育科技", "网络安全", "其他"],
            "文章数": [320, 280, 240, 200, 160, 120, 80, 100]
        }
        df_topics = pd.DataFrame(topic_data)
        
        fig1 = px.pie(
            df_topics,
            values='文章数',
            names='话题',
            title='话题分布',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 情感趋势图
        dates = pd.date_range(start_date, end_date, freq='D')
        sentiment_data = {
            "日期": dates,
            "情感分数": 0.3 + 0.4 * (pd.Series(range(len(dates))) / len(dates)) + 0.1 * np.random.randn(len(dates)),
            "文章数": np.random.randint(30, 100, len(dates))
        }
        df_sentiment = pd.DataFrame(sentiment_data)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_sentiment["日期"],
            y=df_sentiment["情感分数"],
            mode='lines',
            name='情感分数',
            line=dict(color='royalblue', width=3),
            fill='tozeroy',
            fillcolor='rgba(65, 105, 225, 0.1)'
        ))
        
        fig2.update_layout(
            title='情感趋势',
            xaxis_title='日期',
            yaxis_title='情感分数',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # 实时数据预览
    st.subheader("📰 实时新闻预览")
    
    sample_articles = [
        {
            "标题": "欧盟通过新的人工智能监管法案",
            "来源": "Reuters",
            "时间": "2小时前",
            "情感": "正面",
            "话题": "AI监管"
        },
        {
            "标题": "全球芯片供应紧张局势缓解",
            "来源": "华尔街日报",
            "时间": "5小时前",
            "情感": "中性",
            "话题": "芯片竞争"
        },
        {
            "标题": "气候峰会达成历史性减排协议",
            "来源": "BBC",
            "时间": "1天前",
            "情感": "正面",
            "话题": "气候政策"
        },
        {
            "标题": "科技巨头发布季度财报",
            "来源": "CNN",
            "时间": "2天前",
            "情感": "混合",
            "话题": "经济复苏"
        }
    ]
    
    for article in sample_articles:
        with st.expander(f"{article['标题']} ({article['来源']})"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("情感", article['情感'])
            with col2:
                st.metric("话题", article['话题'])
            with col3:
                st.metric("时间", article['时间'])
            
            if st.button(f"分析全文", key=f"btn_{article['标题'][:10]}"):
                st.info(f"正在分析文章: {article['标题']}")
                st.success("分析完成！关键实体: AI, 监管, 政策")

with tab2:
    st.header("话题详细分析")
    
    # 话题选择器
    selected_topic = st.selectbox(
        "选择要分析的话题",
        ["AI监管与伦理", "气候变化政策", "全球芯片竞争", "经济复苏", "医疗科技创新", "教育数字化转型", "网络安全挑战"],
        index=0
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 话题热度变化
        st.subheader(f"话题热度趋势: {selected_topic}")
        
        # 生成示例趋势数据
        days = 30
        dates = [start_date + timedelta(days=i) for i in range(days)]
        base_trend = np.linspace(0.3, 0.8, days)
        noise = np.random.normal(0, 0.1, days)
        heat_scores = np.clip(base_trend + noise, 0, 1)
        
        trend_df = pd.DataFrame({
            "日期": dates,
            "热度分数": heat_scores,
            "文章数量": np.random.randint(10, 50, days)
        })
        
        fig_trend = px.line(
            trend_df,
            x="日期",
            y="热度分数",
            title=f"{selected_topic} 热度趋势",
            markers=True
        )
        
        # 添加文章数量柱状图
        fig_trend.add_trace(go.Bar(
            x=trend_df["日期"],
            y=trend_df["文章数量"],
            name="文章数量",
            yaxis="y2",
            opacity=0.3
        ))
        
        fig_trend.update_layout(
            yaxis2=dict(
                title="文章数量",
                overlaying="y",
                side="right"
            ),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        # 话题统计信息
        st.subheader("话题统计")
        
        stats_data = {
            "指标": ["总文章数", "平均情感", "峰值热度", "持续时间", "相关话题数", "媒体覆盖率"],
            "数值": ["320篇", "+0.25", "0.89", "15天", "3个", "87%"]
        }
        
        st.dataframe(
            pd.DataFrame(stats_data),
            use_container_width=True,
            hide_index=True
        )
        
        # 话题关键词
        st.subheader("🔑 关键词云")
        
        if selected_topic == "AI监管与伦理":
            keywords = ["AI", "监管", "伦理", "算法", "透明度", "责任", "政策", "法案", "合规", "治理"]
        elif selected_topic == "气候变化政策":
            keywords = ["气候", "环保", "减排", "能源", "可持续", "碳", "绿色", "政策", "协议", "生态"]
        else:
            keywords = ["技术", "创新", "发展", "市场", "竞争", "投资", "战略", "未来", "挑战", "机遇"]
        
        # 创建关键词展示
        keyword_html = "<div style='line-height:2.5;'>"
        for kw in keywords:
            size = np.random.randint(14, 24)
            color = f"hsl({np.random.randint(0, 360)}, 70%, 60%)"
            keyword_html += f"<span style='font-size:{size}px; color:{color}; margin:5px; padding:5px 10px; background:#f0f0f0; border-radius:15px; display:inline-block;'>{kw}</span>"
        keyword_html += "</div>"
        
        st.markdown(keyword_html, unsafe_allow_html=True)
    
    # 相关文章列表
    st.subheader("📄 相关文章")
    
    related_articles = [
        {"title": f"关于{selected_topic}的最新研究进展", "source": "Science Daily", "date": "2024-01-15", "sentiment": 0.6},
        {"title": f"专家解读{selected_topic}的未来趋势", "source": "Tech Review", "date": "2024-01-12", "sentiment": 0.4},
        {"title": f"政策制定者讨论{selected_topic}实施方案", "source": "Policy Journal", "date": "2024-01-10", "sentiment": 0.2},
        {"title": f"企业如何应对{selected_topic}带来的挑战", "source": "Business Weekly", "date": "2024-01-08", "sentiment": 0.3},
    ]
    
    for i, article in enumerate(related_articles):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{article['title']}**")
                st.caption(f"来源: {article['source']} | 日期: {article['date']}")
            with col2:
                sentiment_color = "green" if article['sentiment'] > 0 else "red" if article['sentiment'] < 0 else "gray"
                st.markdown(f"<span style='color:{sentiment_color};'>情感: {article['sentiment']:+.2f}</span>", unsafe_allow_html=True)
            with col3:
                if st.button("查看详情", key=f"detail_{i}"):
                    st.session_state[f"show_detail_{i}"] = not st.session_state.get(f"show_detail_{i}", False)
            
            if st.session_state.get(f"show_detail_{i}", False):
                st.info(f"这是关于{selected_topic}的详细分析文章，讨论了当前的热点问题和未来发展方向。")
            st.divider()

with tab3:
    st.header("趋势追踪与预测")
    
    # 多话题对比
    st.subheader("多话题热度对比")
    
    topics_comparison = ["AI监管", "气候政策", "芯片竞争", "经济复苏", "医疗突破"]
    comparison_data = []
    
    for topic in topics_comparison:
        base = np.random.uniform(0.3, 0.7)
        trend = np.random.uniform(-0.2, 0.2)
        days = 30
        values = [base + trend * (i/days) + np.random.normal(0, 0.05) for i in range(days)]
        values = np.clip(values, 0, 1)
        
        for i, val in enumerate(values):
            comparison_data.append({
                "日期": start_date + timedelta(days=i),
                "热度": val,
                "话题": topic
            })
    
    df_comparison = pd.DataFrame(comparison_data)
    
    fig_comparison = px.line(
        df_comparison,
        x="日期",
        y="热度",
        color="话题",
        title="多话题热度对比",
        line_shape="spline"
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # 预测分析
    st.subheader("📈 趋势预测")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 未来7天预测
        - **AI监管**: ↗ 上升趋势 (置信度: 85%)
        - **气候政策**: → 保持稳定 (置信度: 75%)
        - **芯片竞争**: ↘ 下降趋势 (置信度: 70%)
        - **经济复苏**: ↗ 缓慢上升 (置信度: 65%)
        """)
    
    with col2:
        # 预测图表
        future_dates = [end_date + timedelta(days=i) for i in range(1, 8)]
        predictions = {
            "AI监管": [0.7, 0.72, 0.75, 0.77, 0.78, 0.79, 0.8],
            "气候政策": [0.6, 0.61, 0.61, 0.62, 0.62, 0.63, 0.63],
            "芯片竞争": [0.5, 0.49, 0.48, 0.47, 0.46, 0.45, 0.44]
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
            title="话题热度预测",
            xaxis_title="日期",
            yaxis_title="预测热度",
            template="plotly_white"
        )
        
        st.plotly_chart(fig_predict, use_container_width=True)

with tab4:
    st.header("分析报告")
    
    # 报告生成选项
    col1, col2, col3 = st.columns(3)
    
    with col1:
        report_type = st.selectbox(
            "报告类型",
            ["日报", "周报", "月报", "专题报告"]
        )
    
    with col2:
        report_format = st.selectbox(
            "导出格式",
            ["HTML", "PDF", "Markdown", "Word"]
        )
    
    with col3:
        include_charts = st.checkbox("包含图表", value=True)
        include_data = st.checkbox("包含原始数据", value=False)
    
    # 生成报告按钮
    if st.button("📄 生成分析报告", type="primary", use_container_width=True):
        with st.spinner("正在生成报告..."):
            # 模拟报告生成过程
            import time
            time.sleep(2)
            
            # 显示报告预览
            st.success("报告生成成功！")
            
            # 报告内容
            st.subheader("报告预览")
            
            report_content = f"""
            # 新闻趋势分析报告
            **报告类型**: {report_type}
            **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            **分析时段**: {start_date} 至 {end_date}
            
            ## 执行摘要
            在分析期间，系统共处理了1,254篇新闻文章，识别出8个核心话题。整体情感倾向为略微正面(+0.15)。
            
            ## 核心发现
            1. **AI监管话题热度持续上升**，在欧盟法案通过后热度增长45%
            2. **气候政策话题情感最为积极**，平均情感分数达+0.60
            3. **芯片竞争话题呈现地区性差异**，不同地区报道角度不同
            
            ## 详细分析
            ### 1. 话题分布
            - AI监管与伦理: 320篇文章 (25.5%)
            - 气候变化政策: 280篇文章 (22.3%)
            - 全球芯片竞争: 240篇文章 (19.1%)
            - 其他话题: 414篇文章 (33.0%)
            
            ### 2. 情感分析
            - 整体平均情感: +0.15
            - 正面文章比例: 42%
            - 负面文章比例: 28%
            - 中性文章比例: 30%
            
            ### 3. 趋势预测
            预计未来一周AI监管话题热度将继续上升，而芯片竞争话题可能降温。
            
            ## 建议
            1. 持续关注AI监管政策的后续发展
            2. 加强对气候政策相关投资机会的研究
            3. 监控芯片供应链的变化对行业的影响
            
            ---
            *本报告由新闻趋势分析系统自动生成*
            """
            
            st.markdown(report_content)
            
            # 导出选项
            st.download_button(
                label="📥 下载报告",
                data=report_content,
                file_name=f"news_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )

# 页脚
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption("© 2024 新闻趋势分析系统")
with footer_col2:
    st.caption("版本: v1.0.0")
with footer_col3:
    st.caption("[查看源代码](https://github.com/yourusername/news-trend-analysis)")

# 添加一些样式
st.markdown("""
<style>
    /* 主标题样式 */
    .stTitle {
        color: #1f77b4;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* 按钮样式 */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    
    /* 指标卡片样式 */
    .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 标签页激活状态 */
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

# 会话状态初始化
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.analysis_results = None

# 运行分析
if analyze_button:
    with st.spinner("正在分析数据..."):
        import time
        progress_bar = st.progress(0)
        
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
        
        st.session_state.data_loaded = True
        st.session_state.analysis_results = {
            "topics": ["AI监管", "气候政策", "芯片竞争"],
            "sentiment": 0.15,
            "articles_analyzed": 1254
        }
        
        st.success("分析完成！")
        st.rerun()

if __name__ == "__main__":
    # 在开发环境中，Streamlit会自动运行此脚本
    # 这里可以添加一些开发时的特定代码
    if st.secrets.get("ENV") == "development":
        st.sidebar.info("开发模式")
