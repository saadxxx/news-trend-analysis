"""
Visualization Chart Generator: Creates various analysis charts.
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
    """Visualization chart generator"""
    
    def __init__(self, output_dir: str = "docs/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def generate_wordcloud(self, 
                          word_freq: Dict[str, int], 
                          title: str = "Topic wordcloud",
                          filename: str = "wordcloud.png") -> str:
        """
        Generate word cloud chart
        
        Parameters:
            word_freq: Word frequency dictionary {word: frequency}
            title: Chart title
            filename: Save file name
            
        Returns:
            str: Saved file path
        """
        if not word_freq:
            logger.warning("Word frequency data is empty, cannot generate word cloud")
            return ""
        
        # Create word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100,
            contour_width=1,
            contour_color='steelblue'
        ).generate_from_frequencies(word_freq)
        
        # Draw
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Save
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"Word cloud chart saved: {filepath}")
        return str(filepath)
    
    def generate_trend_heatmap(self,
                              topic_trends: pd.DataFrame,
                              filename: str = "trend_heatmap.png") -> str:
        """
        Generate topic trend heatmap
        
        Parameters:
            topic_trends: DataFrame, index is date, columns are topics, values are heat
            filename: Save file name
            
        Returns:
            str: Saved file path
        """
        if topic_trends.empty:
            logger.warning("Trend data is empty, cannot generate heatmap")
            return ""
        
        # Create heatmap
        plt.figure(figsize=(14, 8))
        
        # Use seaborn heatmap
        sns.heatmap(
            topic_trends.T,  # Transpose, put topics on y-axis
            cmap='YlOrRd',
            linewidths=0.5,
            linecolor='gray',
            cbar_kws={'label': 'Heat score'}
        )
        
        plt.title('Topic Trend Heatmap', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Topic', fontsize=12)
        plt.xticks(rotation=45)
        
        # Save
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Trend heatmap saved: {filepath}")
        return str(filepath)
    
    def generate_sentiment_timeline(self,
                                   sentiment_data: pd.DataFrame,
                                   filename: str = "sentiment_timeline.html") -> str:
        """
        Generate sentiment timeline chart (interactive)
        
        Parameters:
            sentiment_data: DataFrame, contains date, sentiment_score, article_count columns
            filename: Save file name
            
        Returns:
            str: Saved file path
        """
        if sentiment_data.empty:
            logger.warning("Sentiment data is empty, cannot generate timeline chart")
            return ""
        
        # Create interactive chart
        fig = go.Figure()
        
        # Add sentiment score line
        fig.add_trace(go.Scatter(
            x=sentiment_data['date'],
            y=sentiment_data['sentiment_score'],
            mode='lines+markers',
            name='Sentiment Score',
            line=dict(color='royalblue', width=3),
            marker=dict(size=8),
            hovertemplate='Date: %{x}<br>Sentiment Score: %{y:.2f}<extra></extra>'
        ))
        
        # Add article count bar chart (secondary axis)
        fig.add_trace(go.Bar(
            x=sentiment_data['date'],
            y=sentiment_data['article_count'],
            name='Article Count',
            yaxis='y2',
            marker_color='rgba(255, 165, 0, 0.6)',
            opacity=0.7,
            hovertemplate='Date: %{x}<br>Article Count: %{y}<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': 'News Sentiment Trend Timeline',
                'font': {'size': 20, 'weight': 'bold'}
            },
            xaxis=dict(
                title='Date',
                tickangle=45,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='Sentiment Score',
                titlefont=dict(color='royalblue'),
                tickfont=dict(color='royalblue'),
                gridcolor='lightgray',
                range=[-1, 1]  # Sentiment score range
            ),
            yaxis2=dict(
                title='Article Count',
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
        
        # Save as HTML (interactive)
        filepath = self.output_dir / filename
        fig.write_html(filepath)
        
        # Also save as static image
        static_path = self.output_dir / "sentiment_timeline.png"
        fig.write_image(str(static_path), width=1200, height=500)
        
        logger.info(f"Sentiment timeline chart saved: {filepath}")
        return str(filepath)
    
    def generate_topic_distribution(self,
                                   topic_data: pd.DataFrame,
                                   filename: str = "topic_distribution.html") -> str:
        """
        Generate topic distribution chart
        
        Parameters:
            topic_data: DataFrame, contains topic_name, article_count, avg_sentiment columns
            filename: Save file name
            
        Returns:
            str: Saved file path
        """
        if topic_data.empty:
            logger.warning("Topic data is empty, cannot generate distribution chart")
            return ""
        
        # Create bubble chart: size represents article count, color represents sentiment
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
            title='Topic Distribution Bubble Chart'
        )
        
        fig.update_layout(
            xaxis_title='Topic',
            yaxis_title='Article Count',
            coloraxis_colorbar=dict(
                title='Average Sentiment',
                titleside='right'
            ),
            height=500,
            template='plotly_white'
        )
        
        # Save
        filepath = self.output_dir / filename
        fig.write_html(filepath)
        
        logger.info(f"Topic distribution chart saved: {filepath}")
        return str(filepath)
    
    def generate_all_visualizations(self, sample_data: bool = True) -> Dict[str, str]:
        """
        Generate all visualization charts
        
        Parameters:
            sample_data: Whether to use sample data
            
        Returns:
            Dict[str, str]: Generated file path dictionary
        """
        results = {}
        
        if sample_data:
            # Generate sample data
            word_freq, topic_trends, sentiment_data, topic_data = self._create_sample_data()
        else:
            # Here should load data from actual analysis results
            # For simplicity, we use sample data
            word_freq, topic_trends, sentiment_data, topic_data = self._create_sample_data()
        
        # Generate all charts
        results['wordcloud'] = self.generate_wordcloud(
            word_freq, 
            title="News Topic Word Cloud - Jan 2024"
        )
        
        results['heatmap'] = self.generate_trend_heatmap(topic_trends)
        
        results['sentiment_timeline'] = self.generate_sentiment_timeline(sentiment_data)
        
        results['topic_distribution'] = self.generate_topic_distribution(topic_data)
        
        # Generate dashboard screenshot (simulated)
        self._generate_dashboard_preview()
        
        return results
    
    def _create_sample_data(self):
        """Create sample data for demonstration"""
        try:
            import pandas as pd
            import numpy as np
            
            # 1. Word frequency data
            word_freq = {
                'AI': 150, 'Artificial Intelligence': 120, 'Machine Learning': 100, 'Deep Learning': 85,
                'Regulation': 80, 'Policy': 75, 'Ethics': 70, 'Innovation': 65
            }
            
            # 2. Topic trend data
            dates = pd.date_range('2024-01-01', '2024-01-10', freq='D')
            topics = ['AI Regulation', 'Climate Policy', 'Chip Competition']
            
            np.random.seed(42)
            trend_data = {}
            for topic in topics:
                base = np.random.uniform(0.3, 0.7)
                values = np.clip(base + np.random.normal(0, 0.1, len(dates)), 0, 1)
                trend_data[topic] = values
            
            topic_trends = pd.DataFrame(trend_data, index=dates)
            
            # 3. Sentiment timeline data
            sentiment_dates = pd.date_range('2024-01-01', '2024-01-10', freq='D')
            sentiment_data = pd.DataFrame({
                'date': sentiment_dates,
                'sentiment_score': np.sin(np.linspace(0, 4*np.pi, len(sentiment_dates))) * 0.8,
                'article_count': np.random.randint(50, 200, len(sentiment_dates))
            })
            
            # 4. Topic distribution data
            topic_data = pd.DataFrame({
                'topic_name': topics,
                'article_count': [320, 280, 240],
                'avg_sentiment': [0.2, 0.6, -0.3]
            })
            
            return word_freq, topic_trends, sentiment_data, topic_data
            
        except Exception as e:
            print(f"Error creating sample data: {e}")
            return {}, pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    def _generate_dashboard_preview(self):
        """Generate dashboard preview image (simulated)"""
        # Create a simple dashboard preview
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Simulate dashboard layout
        axes[0, 0].text(0.5, 0.5, 'Topic Selector\n\n• AI Regulation\n• Climate Policy\n• Chip Competition\n• Economic Recovery',
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        axes[0, 0].set_title('Control Panel', fontweight='bold')
        axes[0, 0].axis('off')
        
        axes[0, 1].text(0.5, 0.5, 'Real-time Statistics\n\nTotal Articles: 1,250\nNew Today: 42\nSentiment Trend: ↗ Positive',
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
        axes[0, 1].set_title('Data Overview', fontweight='bold')
        axes[0, 1].axis('off')
        
        axes[1, 0].text(0.5, 0.5, 'Topic Heat Trend Chart\n\n(Interactive chart shown here)',
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat"))
        axes[1, 0].set_title('Trend Analysis', fontweight='bold')
        axes[1, 0].axis('off')
        
        axes[1, 1].text(0.5, 0.5, 'Sentiment Distribution Chart\n\nPositive: 45%\nNeutral: 35%\nNegative: 20%',
                       ha='center', va='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))
        axes[1, 1].set_title('Sentiment Analysis', fontweight='bold')
        axes[1, 1].axis('off')
        
        plt.suptitle('News Trend Analysis Dashboard - Streamlit App Preview', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        filepath = self.output_dir / "dashboard_preview.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Dashboard preview image saved: {filepath}")


# Usage example
if __name__ == "__main__":
    # Set up logging
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    # Create visualization generator
    viz = VisualizationGenerator()
    
    # Generate all visualization charts
    print("Generating visualization charts...")
    results = viz.generate_all_visualizations(sample_data=True)
    
    print("\nGenerated files:")
    for chart_type, filepath in results.items():
        if filepath:
            print(f"  {chart_type}: {filepath}")
    
    print("\nDashboard preview image saved: docs/images/dashboard_preview.png")
