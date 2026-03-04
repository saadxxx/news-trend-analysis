"""
Text deduplication module: Remove duplicate or highly similar news articles based on similarity detection.
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
    """News article data class"""
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
    """News deduplicator"""
    
    def __init__(self, similarity_threshold: float = 0.8):
        """
        Initialize deduplicator
        
        Args:
            similarity_threshold: Similarity threshold, above which articles are considered duplicates
        """
        self.threshold = similarity_threshold
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def find_duplicates(self, articles: List[NewsArticle]) -> List[Set[str]]:
        """
        Identify duplicate article groups
        
        Args:
            articles: List of NewsArticle objects
            
        Returns:
            List[Set[str]]: List of article ID sets for each duplicate group
        """
        if len(articles) <= 1:
            return []
        
        # Extract text content (title + first 100 characters of content)
        texts = [
            f"{article.title} {article.content[:100]}" 
            for article in articles
        ]
        
        # Calculate TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        # Calculate cosine similarity matrix
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Identify duplicate groups
        duplicate_groups = []
        visited = set()
        
        for i in range(len(articles)):
            if i in visited:
                continue
                
            # Find all articles with similarity above threshold to article i
            duplicates = {i}
            for j in range(i + 1, len(articles)):
                if similarity_matrix[i, j] >= self.threshold:
                    duplicates.add(j)
                    visited.add(j)
            
            if len(duplicates) > 1:
                # Convert to article ID set
                article_ids = {articles[idx].article_id for idx in duplicates}
                duplicate_groups.append(article_ids)
                visited.update(duplicates)
        
        return duplicate_groups
    
    def remove_duplicates(self, articles: List[NewsArticle]) -> Tuple[List[NewsArticle], List[Set[str]]]:
        """
        Remove duplicate articles, keeping the earliest one in each group
        
        Args:
            articles: List of NewsArticle objects
            
        Returns:
            Tuple: (Deduplicated article list, duplicate group list)
        """
        duplicate_groups = self.find_duplicates(articles)
        
        if not duplicate_groups:
            return articles, []
        
        # Create mapping from article ID to index
        id_to_index = {article.article_id: i for i, article in enumerate(articles)}
        
        # Determine which articles to keep
        articles_to_keep = set(range(len(articles)))
        articles_to_remove = set()
        
        for group in duplicate_groups:
            # Convert to indices
            indices = [id_to_index[article_id] for article_id in group]
            
            # Sort by date, keep the earliest
            sorted_indices = sorted(
                indices, 
                key=lambda idx: articles[idx].date
            )
            
            # Keep the earliest article, remove others
            articles_to_keep.difference_update(sorted_indices[1:])
            articles_to_remove.update(sorted_indices[1:])
        
        # Build result
        filtered_articles = [
            articles[i] for i in sorted(articles_to_keep)
        ]
        
        logger.info(f"Deduplication completed: Original {len(articles)} articles, After deduplication {len(filtered_articles)} articles")
        
        return filtered_articles, duplicate_groups


# Usage example
if __name__ == "__main__":
    # Create sample articles
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
    
    print(f"Original article count: {len(articles)}")
    print(f"Deduplicated article count: {len(unique_articles)}")
    print(f"Duplicate groups found: {duplicates}")
