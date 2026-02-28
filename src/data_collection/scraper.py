"""
新闻数据采集模块。
支持多源、可扩展、带错误处理和速率限制。
News data collection module.
Supports multi-source, scalable, with error handling and rate limiting.
"""
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from .utils import get_user_agent, validate_date

logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self, config_path="config/news_sources.json"):
        with open(config_path, 'r') as f:
            self.sources = json.load(f)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': get_user_agent()})
        
    def fetch_article(self, url):
        """获取单篇文章内容"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            # 示例解析逻辑（需根据实际网站结构调整）
            title = soup.find('h1').get_text(strip=True) if soup.find('h1') else ""
            body = ' '.join([p.get_text() for p in soup.find_all('p')])
            return {'title': title, 'body': body, 'url': url, 'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S')}
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def scrape_all(self, max_articles=100):
        """从所有配置源抓取文章"""
        articles = []
        for source in self.sources:
            logger.info(f"Scraping {source['name']}")
            for url in source['urls'][:max_articles]:
                article = self.fetch_article(url)
                if article:
                    articles.append(article)
                time.sleep(1)  # 礼貌延迟
        return articles

if __name__ == "__main__":
    scraper = NewsScraper()
    data = scraper.scrape_all(max_articles=10)
    print(f"Collected {len(data)} articles.")
