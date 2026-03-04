"""
News data collection module.
Supports multi-source, scalable, with error handling and rate limiting.
"""
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import random
import hashlib
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class Article:
    """Article data structure"""
    title: str
    content: str
    source: str
    url: str
    published_date: str
    fetched_at: str
    article_id: str = None
    
    def __post_init__(self):
        if not self.article_id:
            # Generate a unique ID based on title and source
            self.article_id = hashlib.md5(
                f"{self.title}_{self.source}_{self.published_date}".encode()
            ).hexdigest()[:12]

class RateLimiter:
    """Rate limiter for polite scraping"""
    
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.request_times = []
        self.min_interval = 60.0 / requests_per_minute
    
    def wait_if_needed(self):
        """Wait if we're making requests too fast"""
        now = time.time()
        
        # Remove timestamps older than 60 seconds
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        if len(self.request_times) >= self.requests_per_minute:
            # Calculate how long to wait
            oldest = self.request_times[0]
            wait_time = 60 - (now - oldest)
            if wait_time > 0:
                logger.debug(f"Rate limiting: waiting {wait_time:.2f} seconds")
                time.sleep(wait_time)
                self.request_times = []
        
        # Add jitter to avoid detection
        jitter = random.uniform(0.1, 0.5)
        time.sleep(jitter)
        
        self.request_times.append(time.time())

class NewsScraper:
    """Main news scraper class with multi-source support"""
    
    def __init__(self, config_path: str = "config/news_sources.json"):
        """
        Initialize the news scraper
        
        Args:
            config_path: Path to JSON configuration file with news sources
        """
        self.config_path = config_path
        self.load_config()
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(requests_per_minute=20)
        self.setup_session_headers()
        
    def load_config(self):
        """Load news source configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.sources = json.load(f)
            logger.info(f"Loaded {len(self.sources)} news sources from {self.config_path}")
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}, using default sources")
            self.sources = self.get_default_sources()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing config file: {e}")
            raise
    
    def get_default_sources(self) -> List[Dict]:
        """Get default news sources if config file is missing"""
        return [
            {
                "name": "Reuters",
                "base_url": "https://www.reuters.com",
                "type": "rss",
                "urls": ["https://www.reuters.com/world/"],
                "selectors": {
                    "article": "article",
                    "title": "h1",
                    "content": "p",
                    "date": "time"
                }
            },
            {
                "name": "BBC News",
                "base_url": "https://www.bbc.com",
                "type": "html",
                "urls": ["https://www.bbc.com/news"],
                "selectors": {
                    "article": "div[data-entityid='container-top-stories#1']",
                    "title": "h3",
                    "content": "p",
                    "date": "time"
                }
            }
        ]
    
    def setup_session_headers(self):
        """Setup HTTP session headers to mimic a real browser"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def fetch_article(self, url: str, source_config: Dict) -> Optional[Article]:
        """
        Fetch and parse a single article
        
        Args:
            url: Article URL
            source_config: Configuration for the news source
            
        Returns:
            Article object or None if failed
        """
        try:
            # Apply rate limiting
            self.rate_limiter.wait_if_needed()
            
            logger.debug(f"Fetching article: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract article data using configured selectors
            title = self.extract_text(soup, source_config.get('selectors', {}).get('title', 'h1'))
            content = self.extract_content(soup, source_config.get('selectors', {}).get('content', 'p'))
            date = self.extract_date(soup, source_config.get('selectors', {}).get('date', 'time'))
            
            if not title or not content:
                logger.warning(f"Incomplete article data from {url}")
                return None
            
            # Create Article object
            article = Article(
                title=title.strip(),
                content=content.strip(),
                source=source_config['name'],
                url=url,
                published_date=date or datetime.now().strftime('%Y-%m-%d'),
                fetched_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            logger.info(f"Successfully fetched: {article.title[:50]}...")
            return article
            
        except requests.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
        
        return None
    
    def extract_text(self, soup: BeautifulSoup, selector: str) -> str:
        """Extract text using CSS selector"""
        try:
            element = soup.select_one(selector)
            return element.get_text(strip=True) if element else ""
        except Exception:
            return ""
    
    def extract_content(self, soup: BeautifulSoup, selector: str) -> str:
        """Extract article content"""
        try:
            paragraphs = soup.select(selector)
            # Combine first 10 paragraphs as content
            content = ' '.join([p.get_text(strip=True) for p in paragraphs[:10]])
            return content[:2000]  # Limit content length
        except Exception:
            return ""
    
    def extract_date(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract publication date"""
        try:
            element = soup.select_one(selector)
            if element:
                # Try to get datetime attribute first
                datetime_attr = element.get('datetime')
                if datetime_attr:
                    return datetime_attr[:10]  # YYYY-MM-DD
                return element.get_text(strip=True)[:10]
        except Exception:
            pass
        return None
    
    def discover_article_urls(self, source_config: Dict, max_urls: int = 20) -> List[str]:
        """
        Discover article URLs from a news source homepage
        
        Args:
            source_config: News source configuration
            max_urls: Maximum number of URLs to discover
            
        Returns:
            List of article URLs
        """
        urls = []
        try:
            for base_url in source_config.get('urls', []):
                self.rate_limiter.wait_if_needed()
                
                response = self.session.get(base_url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find article links
                article_selector = source_config.get('selectors', {}).get('article', 'a')
                links = soup.select(article_selector)
                
                for link in links[:max_urls]:
                    href = link.get('href')
                    if href:
                        # Convert relative URLs to absolute
                        full_url = urljoin(base_url, href)
                        if full_url not in urls and self.is_article_url(full_url):
                            urls.append(full_url)
                
                logger.info(f"Discovered {len(urls)} article URLs from {source_config['name']}")
                
        except Exception as e:
            logger.error(f"Error discovering URLs from {source_config['name']}: {e}")
        
        return urls[:max_urls]
    
    def is_article_url(self, url: str) -> bool:
        """Check if URL looks like an article URL"""
        article_indicators = ['/article/', '/news/', '/story/', '/2024/', '/blog/']
        return any(indicator in url.lower() for indicator in article_indicators)
    
    def scrape_all(self, max_articles_per_source: int = 10) -> List[Article]:
        """
        Scrape articles from all configured sources
        
        Args:
            max_articles_per_source: Maximum articles to scrape per source
            
        Returns:
            List of Article objects
        """
        all_articles = []
        
        for source_config in self.sources:
            try:
                logger.info(f"Scraping from source: {source_config['name']}")
                
                # Discover article URLs
                article_urls = self.discover_article_urls(
                    source_config, 
                    max_urls=max_articles_per_source
                )
                
                # Fetch articles
                for url in article_urls:
                    article = self.fetch_article(url, source_config)
                    if article:
                        all_articles.append(article)
                    
                    # Check if we've reached the limit
                    if len(all_articles) >= max_articles_per_source * len(self.sources):
                        break
                
                logger.info(f"Completed scraping from {source_config['name']}: {len(article_urls)} URLs processed")
                
            except Exception as e:
                logger.error(f"Error scraping from {source_config['name']}: {e}")
                continue
        
        logger.info(f"Scraping completed. Total articles collected: {len(all_articles)}")
        return all_articles
    
    def save_articles(self, articles: List[Article], output_path: str = "data/articles.json"):
        """Save articles to JSON file"""
        try:
            # Convert articles to dictionaries
            articles_data = []
            for article in articles:
                article_dict = {
                    'article_id': article.article_id,
                    'title': article.title,
                    'content': article.content,
                    'source': article.source,
                    'url': article.url,
                    'published_date': article.published_date,
                    'fetched_at': article.fetched_at
                }
                articles_data.append(article_dict)
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(articles)} articles to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving articles: {e}")


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create scraper instance
    scraper = NewsScraper()
    
    # Scrape articles
    articles = scraper.scrape_all(max_articles_per_source=5)
    
    # Save results
    if articles:
        scraper.save_articles(articles, "data/articles.json")
        print(f"Successfully collected {len(articles)} articles.")
        
        # Display sample articles
        print("\nSample articles collected:")
        for i, article in enumerate(articles[:3], 1):
            print(f"\n{i}. {article.title}")
            print(f"   Source: {article.source}")
            print(f"   Date: {article.published_date}")
            print(f"   URL: {article.url}")
            print(f"   Preview: {article.content[:100]}...")
    else:
        print("No articles were collected.")
