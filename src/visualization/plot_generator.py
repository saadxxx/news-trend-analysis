"""
可视化图表生成器：创建各种分析图表。
"""
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class VisualizationGenerator:
    """可视化图表生成器"""
    
    def __init__(self, output_dir: str = "docs/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置matplotlib样式
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def generate_wordcloud(self, 
                          word_freq: Dict[str, int], 
                          title: str = "主题词云",
                          filename: str = "wordcloud.png") -> str:
        """
        生成词云图
        
        参数:
            word_freq: 词频字典 {word: frequency}
            title: 图表标题
            filename: 保存文件名
            
        返回:
            str: 保存的文件路径
        """
        if not word_freq:
            logger.warning("词频数据为空，无法生成词云")
            return ""
        
        # 创建词云
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100,
            contour_width=1,
            contour_color='steelblue'
        ).generate_from_frequencies(word_freq)
        
        # 绘制
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        
        # 保存
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"词云图已保存: {filepath}")
        return str(filepath)
    
    def generate_trend_heatmap(self,
                              topic_trends: pd.DataFrame,
                              filename: str = "trend_heatmap.png") -> str:
        """
        生成话题趋势热力图
        
        参数:
            topic_trends: DataFrame，索引为日期，列为话题，值为热度
            filename: 保存文件名
            
        返回:
            str: 保存的文件路径
        """
        if topic_trends.empty:
            logger.warning("趋势数据为空，无法生成热力图")
            return ""
        
        # 创建热力图
        plt.figure(figsize=(14, 8))
        
        # 使用seaborn热力图
        sns.heatmap(
            topic_trends.T,  # 转置，使话题在y轴
            cmap='YlOrRd',
            linewidths=0.5,
            linecolor='gray',
            cbar_kws={'label': '热度分数'}
        )
        
        plt.title('话题热度趋势热力图', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('话题', fontsize=12)
        plt.xticks(rotation=45)
        
        # 保存
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"趋势热力图已保存: {filepath}")
        return str(filepath)
    
    def generate_sentiment_timeline(self,
                                   sentiment_data: pd.DataFrame,
                                   filename: str = "sentiment_timeline.html") -> str:
        """
        生成情感时间线图（交互式）
        
        参数:
            sentiment_data: DataFrame，包含date, sentiment_score, article_count列
            filename: 保存文件名
            
        返回:
            str: 保存的文件路径
        """
        if sentiment_data.empty:
            logger.warning("情感数据为空，无法生成时间线图")
            return ""
        
        # 创建交互式图表
        fig = go.Figure()
        
        # 添加情感分数线
        fig.add_trace(go.Scatter(
            x=sentiment_data['date'],
            y=sentiment_data['sentiment_score'],
            mode='lines+markers',
            name='情感分数',
            line=dict(color='royalblue', width=3),
            marker=dict(size=8),
            hovertemplate='日期: %{x}<br>情感分数: %{y:.2f}<extra></extra>'
        ))
        
        # 添加文章数量柱状图（次坐标轴）
        fig.add_trace(go.Bar(
            x=sentiment_data['date'],
            y=sentiment_data['article_count'],
            name='文章数量',
            yaxis='y2',
            marker_color='rgba(255, 165, 0, 0.6)',
            opacity=0.7,
            hovertemplate='日期: %{x}<br>文章数: %{y}<extra></extra>'
        ))
        
        # 更新布局
        fig.update_layout(
            title={
                'text': '新闻情感趋势时间线',
                'font': {'size': 20, 'weight': 'bold'}
            },
            xaxis=dict(
                title='日期',
                tickangle=45,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='情感分数',
                titlefont=dict(color='royalblue'),
                tickfont=dict(color='royalblue'),
                gridcolor='lightgray',
                range=[-1, 1]  # 情感分数范围
            ),
            yaxis2=dict(
                title='文章数量',
                titlefont=dict(color='orange'),
                tickfont=dict(color='orange'),
                overlaying='y',
                side='right',
                gridcolor='lightgray'
            ),
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # 保存为HTML（交互式）
        filepath = self.output_dir / filename
        fig.write_html(filepath)
        
        # 同时保存为静态图片
        static_path = self.output_dir / "sentiment_timeline.png"
        fig.write_image(str(static_path), width=1200, height=500)
        
        logger.info(f"情感时间线图已保存: {filepath}")
        return str(filepath)
    
    def generate_topic_distribution(self,
                                   topic_data: pd.DataFrame,
                                   filename: str = "topic_distribution.html") -> str:
        """
        生成话题分布图
        
        参数:
            topic_data: DataFrame，包含topic_name, article_count, avg_sentiment列
            filename: 保存文件名
            
        返回:
            str: 保存的文件路径
        """
        if topic_data.empty:
            logger.warning("话题数据为空，无法生成分布图")
            return ""
        
        # 创建气泡图：大小表示文章数量，颜色表示情感
        fig = px.scatter(
            topic_data,
            x='topic_name',
            y='article_count',
            size='article_count',
            color='avg_sentiment',
            color_continuous_scale='RdYlGn',
            hover_name='topic_name',
            hover_data={
                'article_count': True,
                'avg_sentiment': ':.2f',
                'topic_name': False
            },
            size_max=60,
            title='话题分布气泡图'
        )
        
        fig.update_layout(
            xaxis_title='话题',
            yaxis_title='文章数量',
            coloraxis_colorbar=dict(
                title='平均情感',
                titleside='right'
            ),
            height=500,
            template='plotly_white'
        )
        
        # 保存
        filepath = self.output_dir / filename
        fig.write_html(filepath)
        
        logger.info(f"话题分布图已保存: {filepath}")
        return str(filepath)
    
    def generate_all_visualizations(self, sample_data: bool = True) -> Dict[str, str]:
        """
        生成所有可视化图表
        
        参数:
            sample_data: 是否使用示例数据
            
        返回:
            Dict[str, str]: 生成的文件路径字典
        """
        results = {}
        
        if sample_data:
            # 生成示例数据
            word_freq, topic_trends, sentiment_data, topic_data = self._create_sample_data()
        else:
            # 这里应该从实际分析结果加载数据
            # 为简化，我们使用示例数据
            word_freq, topic_trends, sentiment_data, topic_data = self._create_sample_data()
        
        # 生成所有图表
        results['wordcloud'] = self.generate_wordcloud(
            word_freq, 
            title="2024年1月新闻主题词云"
        )
        
        results['heatmap'] = self.generate_trend_heatmap(topic_trends)
        
        results['sentiment_timeline'] = self.generate_sentiment_timeline(sentiment_data)
        
        results['topic_distribution'] = self.generate_topic_distribution(topic_data)
        
        # 生成仪表板截图（模拟）
        self._generate_dashboard_preview()
        
        return results
    
    def _create_sample_data(self):
        """创建示例数据用于演示"""
        
        # 1. 词频数据
        word_freq = {
            'AI': 150, '人工智能': 120, '机器学习': 100, '深度学习': 85,
            '监管': 80, '政策': 75, '伦理': 70, '创新': 65,
            '芯片': 60, '半导体': 55, '投资': 50, '市场': 45,
            '气候': 40, '环保': 35, '能源': 30, '可持续': 25,
            '经济': 20, '增长': 18, '贸易': 15, '全球化': 12
        }
        
        # 2. 话题趋势数据
        dates = pd.date_range('2024-01-01', '2024-01-31', freq='D')
        topics = ['AI监管', '气候政策', '芯片战争', '经济复苏', '医疗突破']
        
        np.random.seed(42)
        trend_data = {}
        for topic in topics:
            # 创建有趋势的随机数据
            base = np.random.uniform(0.3, 0.7)
            trend = np.linspace(0, 1, len(dates)) * np.random.uniform(-0.5, 0.5)
            noise = np.random.normal(0, 0.1, len(dates))
            values = np.clip(base + trend + noise, 0, 1)
            trend_data[topic] = values
        
        topic_trends = pd.DataFrame(trend_data, index=dates)
        
        # 3. 情感时间线数据
        sentiment_dates = pd.date_range('2024-01-01', '2024-01-31', freq='D')
        sentiment_scores = np.sin(np.linspace(0, 4*np.pi, len(sentiment_dates))) * 0.8
        article_counts = np.random.randint(50, 200, len(sentiment_dates))
        
        sentiment_data = pd.DataFrame({
            'date': sentiment_dates,
            'sentiment_score': sentiment_scores,
            'article_count': article_counts
        })
        
        # 4. 话题分布数据
        topic_data = pd.DataFrame({
            'topic_name': topics,
            'article_count': [320, 280, 240, 200, 160],
            'avg_sentiment': [0.2, 0.6, -0.3, 0.4, 0.8],
            'keywords': [
                'AI,监管,伦理,政策',
                '气候,环保,能源,可持续',
                '芯片,半导体,技术,竞争',
                '经济,增长,贸易,市场',
                '医疗,健康,创新,研究'
            ]
        })
        
        return word_freq, topic_trends, sentiment_data, topic_data
    
    def _generate_dashboard_preview(self):
        """生成仪表板预览图（模拟）"""
        # 创建一个简单的仪表板预览
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 模拟仪表板布局
        axes[0, 0].text(0.5, 0.5, '话题选择器\n\n• AI监管\n• 气候政策\n• 芯片战争\n• 经济复苏',
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        axes[0, 0].set_title('控制面板', fontweight='bold')
        axes[0, 0].axis('off')
        
        axes[0, 1].text(0.5, 0.5, '实时数据统计\n\n总文章数: 1,250\n今日新增: 42\n情感趋势: ↗ 正面',
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
        axes[0, 1].set_title('数据概览', fontweight='bold')
        axes[0, 1].axis('off')
        
        axes[1, 0].text(0.5, 0.5, '话题热度趋势图\n\n（此处显示交互式图表）',
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat"))
        axes[1, 0].set_title('趋势分析', fontweight='bold')
        axes[1, 0].axis('off')
        
        axes[1, 1].text(0.5, 0.5, '情感分布图\n\n正面: 45%\n中性: 35%\n负面: 20%',
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        axes[1, 1].set_title('情感分析', fontweight='bold')
        axes[1, 1].axis('off')
        
        plt.suptitle('新闻趋势分析仪表板 - Streamlit应用预览', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        filepath = self.output_dir / "dashboard_preview.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"仪表板预览图已保存: {filepath}")


# 使用示例
if __name__ == "__main__":
    # 设置日志
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    # 创建可视化生成器
    viz = VisualizationGenerator()
    
    # 生成所有可视化图表
    print("正在生成可视化图表...")
    results = viz.generate_all_visualizations(sample_data=True)
    
    print("\n生成的文件:")
    for chart_type, filepath in results.items():
        if filepath:
            print(f"  {chart_type}: {filepath}")
    
    print("\n仪表板预览图已保存: docs/images/dashboard_preview.png")
