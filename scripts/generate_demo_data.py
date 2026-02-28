"""
生成演示数据脚本：创建用于展示的示例分析结果。
"""
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

def generate_demo_results():
    """生成完整的演示结果"""
    
    # 创建输出目录
    output_dir = Path("docs/demo_results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 生成时间范围
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(31)]
    
    # 2. 生成话题分析结果
    topics = [
        {
            "topic_id": 0,
            "topic_name": "AI监管与伦理",
            "keywords": ["AI", "监管", "伦理", "政策", "算法", "透明度"],
            "article_count": 320,
            "avg_sentiment": 0.2,
            "trend": "rising",
            "key_articles": [
                {
                    "title": "欧盟通过全球首部AI监管法案",
                    "source": "Reuters",
                    "date": "2024-01-15",
                    "sentiment": 0.3,
                    "summary": "欧盟议会正式通过《人工智能法案》，为全球AI监管树立新标杆。"
                },
                {
                    "title": "科技巨头承诺负责任AI开发",
                    "source": "TechCrunch",
                    "date": "2024-01-20",
                    "sentiment": 0.5,
                    "summary": "多家科技公司签署AI伦理协议，承诺加强算法透明度。"
                }
            ]
        },
        {
            "topic_id": 1,
            "topic_name": "气候变化政策",
            "keywords": ["气候", "环保", "能源", "可持续", "减排", "碳中和"],
            "article_count": 280,
            "avg_sentiment": 0.6,
            "trend": "stable",
            "key_articles": [
                {
                    "title": "COP29气候大会达成历史性协议",
                    "source": "BBC",
                    "date": "2024-01-10",
                    "sentiment": 0.8,
                    "summary": "各国承诺加大减排力度，设立新的气候基金。"
                }
            ]
        },
        {
            "topic_id": 2,
            "topic_name": "全球芯片竞争",
            "keywords": ["芯片", "半导体", "技术", "竞争", "制造", "供应链"],
            "article_count": 240,
            "avg_sentiment": -0.3,
            "trend": "rising",
            "key_articles": [
                {
                    "title": "美国扩大对华芯片出口限制",
                    "source": "华尔街日报",
                    "date": "2024-01-05",
                    "sentiment": -0.5,
                    "summary": "美国政府宣布新的芯片出口管制措施，引发市场担忧。"
                }
            ]
        }
    ]
    
    # 3. 生成趋势数据
    trend_data = []
    for date in dates:
        for topic in topics:
            # 模拟趋势变化
            base = np.random.uniform(0.3, 0.7)
            if topic["trend"] == "rising":
                trend = (date - start_date).days / 30 * 0.3
            elif topic["trend"] == "declining":
                trend = -(date - start_date).days / 30 * 0.3
            else:
                trend = 0
            
            value = np.clip(base + trend + np.random.normal(0, 0.05), 0, 1)
            
            trend_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "topic": topic["topic_name"],
                "heat_score": round(value, 3),
                "article_count": np.random.randint(5, 20)
            })
    
    # 4. 生成情感分析结果
    sentiment_data = []
    for date in dates:
        # 模拟情感波动
        base_sentiment = np.sin((date - start_date).days / 5) * 0.5
        daily_sentiment = base_sentiment + np.random.normal(0, 0.1)
        
        sentiment_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "avg_sentiment": round(daily_sentiment, 3),
            "positive_ratio": round(0.5 + daily_sentiment * 0.3, 3),
            "negative_ratio": round(0.3 - daily_sentiment * 0.2, 3),
            "neutral_ratio": round(0.2 - daily_sentiment * 0.1, 3),
            "total_articles": np.random.randint(80, 150)
        })
    
    # 5. 保存所有数据
    results = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "time_period": "2024-01-01 to 2024-01-31",
            "total_articles_analyzed": 1250,
            "data_sources": ["Reuters", "BBC", "CNN", "TechCrunch", "华尔街日报"]
        },
        "topics": topics,
        "daily_trends": trend_data,
        "sentiment_analysis": sentiment_data,
        "summary": {
            "dominant_topic": "AI监管与伦理",
            "most_positive_topic": "气候变化政策",
            "most_negative_topic": "全球芯片竞争",
            "overall_sentiment": "slightly_positive",
            "key_insights": [
                "AI监管话题热度持续上升，反映政策关注度增加",
                "气候话题情感最为积极，显示公众乐观态度",
                "芯片竞争话题负面情感突出，反映地缘政治紧张"
            ]
        }
    }
    
    # 保存为JSON
    json_path = output_dir / "analysis_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 保存为CSV（便于查看）
    df_trends = pd.DataFrame(trend_data)
    df_sentiment = pd.DataFrame(sentiment_data)
    
    df_trends.to_csv(output_dir / "daily_trends.csv", index=False, encoding='utf-8')
    df_sentiment.to_csv(output_dir / "sentiment_analysis.csv", index=False, encoding='utf-8')
    
    # 6. 生成README中使用的文字结论
    generate_text_conclusions(results, output_dir)
    
    print(f"演示数据已生成到: {output_dir}")
    print(f"主要文件:")
    print(f"  - analysis_results.json: 完整分析结果")
    print(f"  - daily_trends.csv: 每日趋势数据")
    print(f"  - sentiment_analysis.csv: 情感分析数据")
    print(f"  - text_conclusions.md: 文字结论示例")

def generate_text_conclusions(results, output_dir):
    """生成文字结论示例"""
    
    summary = results["summary"]
    topics = results["topics"]
    
    text = f"""# 新闻趋势分析报告 - 示例结论

## 分析概览
- **分析时段**: {results['metadata']['time_period']}
- **分析文章总数**: {results['metadata']['total_articles_analyzed']:,} 篇
- **数据来源**: {', '.join(results['metadata']['data_sources'])}

## 核心发现

### 1. 主导话题识别
系统成功识别出 **{len(topics)} 个核心话题**，其中：

**{summary['dominant_topic']}** 是讨论最热烈的话题，共涉及 **{topics[0]['article_count']} 篇文章**。该话题的关键词包括：{', '.join(topics[0]['keywords'][:4])}... 热度在分析期内呈现 **上升趋势**，反映了政策制定者和公众对AI监管的持续关注。

### 2. 情感分析洞察
- **最积极话题**: **{summary['most_positive_topic']}** (平均情感分数: +{topics[1]['avg_sentiment']:.2f})
- **最消极话题**: **{summary['most_negative_topic']}** (平均情感分数: {topics[2]['avg_sentiment']:.2f})
- **整体情感倾向**: **略微正面** ({summary['overall_sentiment'].replace('_', ' ')})

### 3. 趋势变化观察
通过对每日数据的分析，发现：
1. **AI监管话题**在1月15日（欧盟法案通过日）后热度显著上升 **45%**
2. **气候政策话题**的情感分数始终保持高位，显示公众对环保议题的乐观态度
3. **芯片竞争话题**的负面情感在1月5日（美国出口限制宣布）达到峰值

### 4. 关键文章摘要
**代表性文章示例**:
- **"{topics[0]['key_articles'][0]['title']}"** ({topics[0]['key_articles'][0]['source']})
  {topics[0]['key_articles'][0]['summary']}
  
- **"{topics[1]['key_articles'][0]['title']}"** ({topics[1]['key_articles'][0]['source']})
  {topics[1]['key_articles'][0]['summary']}

## 结论与建议
基于以上分析，可以得出以下结论：
1. **政策驱动明显**: AI和气候话题的热度与政策事件高度相关
2. **地缘政治影响**: 芯片话题的负面情感反映了当前国际技术竞争的紧张局势
3. **公众参与度高**: 气候话题的积极情感表明公众对可持续发展的高度关注

**建议后续关注**:
- 跟踪AI监管政策的实施效果
- 监测芯片供应链的变化趋势
- 分析气候政策的公众接受度变化

---
*本报告由新闻趋势分析与主题建模管道自动生成*
*生成时间: {results['metadata']['generated_at']}*
"""
    
    md_path = output_dir / "text_conclusions.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    generate_demo_results()
