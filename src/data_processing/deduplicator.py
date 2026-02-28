"""
文本去重模块：基于相似性检测移除重复或高度相似的新闻。
"""
from dataclasses import dataclass
from typing import List, Tuple, Set
import hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging

logger = logging.getLogger(__name__)

@dataclass
class NewsArticle:
    """新闻文章数据类"""
    title: str
    content: str
    source: str
    date: str
    url: str
    article_id: str = None
    
    def __post_init__(self):
        if not self.article_id:
            self.article_id = hashlib.md5(
                f"{self.title}_{self.source}".encode()
            ).hexdigest()[:8]

class Deduplicator:
    """新闻去重器"""
    
    def __init__(self, similarity_threshold: float = 0.8):
        """
        初始化去重器
        
        参数:
            similarity_threshold: 相似度阈值，高于此值视为重复
        """
        self.threshold = similarity_threshold
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def find_duplicates(self, articles: List[NewsArticle]) -> List[Set[str]]:
        """
        识别重复文章组
        
        参数:
            articles: NewsArticle对象列表
            
        返回:
            List[Set[str]]: 每组重复文章的ID集合列表
        """
        if len(articles) <= 1:
            return []
        
        # 提取文本内容（标题+内容的前100字符）
        texts = [
            f"{article.title} {article.content[:100]}" 
            for article in articles
        ]
        
        # 计算TF-IDF向量
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        # 计算余弦相似度矩阵
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # 识别重复组
        duplicate_groups = []
        visited = set()
        
        for i in range(len(articles)):
            if i in visited:
                continue
                
            # 找到与文章i相似度高于阈值的所有文章
            duplicates = {i}
            for j in range(i + 1, len(articles)):
                if similarity_matrix[i, j] >= self.threshold:
                    duplicates.add(j)
                    visited.add(j)
            
            if len(duplicates) > 1:
                # 转换为文章ID集合
                article_ids = {articles[idx].article_id for idx in duplicates}
                duplicate_groups.append(article_ids)
                visited.update(duplicates)
        
        return duplicate_groups
    
    def remove_duplicates(self, articles: List[NewsArticle]) -> Tuple[List[NewsArticle], List[Set[str]]]:
        """
        移除重复文章，保留每个组中最早的一篇
        
        参数:
            articles: NewsArticle对象列表
            
        返回:
            Tuple: (去重后的文章列表, 重复组列表)
        """
        duplicate_groups = self.find_duplicates(articles)
        
        if not duplicate_groups:
            return articles, []
        
        # 创建文章ID到索引的映射
        id_to_index = {article.article_id: i for i, article in enumerate(articles)}
        
        # 确定要保留的文章
        articles_to_keep = set(range(len(articles)))
        articles_to_remove = set()
        
        for group in duplicate_groups:
            # 转换为索引
            indices = [id_to_index[article_id] for article_id in group]
            
            # 按日期排序，保留最早的
            sorted_indices = sorted(
                indices, 
                key=lambda idx: articles[idx].date
            )
            
            # 保留最早的文章，移除其他
            articles_to_keep.difference_update(sorted_indices[1:])
            articles_to_remove.update(sorted_indices[1:])
        
        # 构建结果
        filtered_articles = [
            articles[i] for i in sorted(articles_to_keep)
        ]
        
        logger.info(f"去重完成: 原始 {len(articles)} 篇, 去重后 {len(filtered_articles)} 篇")
        
        return filtered_articles, duplicate_groups


# 使用示例
if __name__ == "__main__":
    # 创建示例文章
    articles = [
        NewsArticle(
            title="Breaking News: Important Event",
            content="This is the content of the important news event.",
            source="Reuters",
            date="2024-01-15",
            url="http://example.com/1"
        ),
        NewsArticle(
            title="Important Event Update",
            content="This is an update about the important news event.",
            source="BBC",
            date="2024-01-15",
            url="http://example.com/2"
        ),
        NewsArticle(
            title="Weather Forecast",
            content="The weather will be sunny tomorrow.",
            source="CNN",
            date="2024-01-15",
            url="http://example.com/3"
        )
    ]
    
    deduplicator = Deduplicator(similarity_threshold=0.7)
    unique_articles, duplicates = deduplicator.remove_duplicates(articles)
    
    print(f"原始文章数: {len(articles)}")
    print(f"去重后文章数: {len(unique_articles)}")
    print(f"发现重复组: {duplicates}")
