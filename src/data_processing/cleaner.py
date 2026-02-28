"""
文本清洗模块：处理原始文本，移除无关字符、标准化格式。
"""
import re
import html
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TextCleaner:
    """清洗新闻文本的类"""
    
    def __init__(self, remove_patterns: Optional[list] = None):
        """
        初始化清洗器
        
        参数:
            remove_patterns: 自定义正则表达式模式列表，用于移除特定文本
        """
        # 默认清洗模式：HTML标签、URL、邮箱、特殊符号、多余空白
        self.default_patterns = [
            r'<[^>]+>',  # HTML标签
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URL
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # 邮箱
            r'[^\w\s.,!?;:\'\"-]',  # 非常规符号（保留基本标点）
            r'\s+',  # 多个空白字符
        ]
        
        self.patterns = self.default_patterns + (remove_patterns or [])
    
    def clean(self, text: str) -> str:
        """
        执行完整的文本清洗流程
        
        参数:
            text: 原始文本字符串
            
        返回:
            str: 清洗后的文本
        """
        if not text or not isinstance(text, str):
            return ""
        
        cleaned = text
        
        # 1. 解码HTML实体（如 &amp; -> &）
        cleaned = html.unescape(cleaned)
        
        # 2. 移除所有匹配模式的内容
        for pattern in self.patterns:
            cleaned = re.sub(pattern, ' ', cleaned)
        
        # 3. 标准化空白字符（多个空格/换行变为单个空格）
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # 4. 去除首尾空白
        cleaned = cleaned.strip()
        
        # 5. 统一引号（可选，针对多语言文本）
        cleaned = self._normalize_quotes(cleaned)
        
        logger.debug(f"文本清洗完成: 原始长度 {len(text)}, 清洗后长度 {len(cleaned)}")
        return cleaned
    
    def clean_batch(self, texts: list) -> list:
        """批量清洗文本列表"""
        return [self.clean(text) for text in texts]
    
    def _normalize_quotes(self, text: str) -> str:
        """将弯引号、全角引号等统一为直引号"""
        # 左弯引号/全角左引号 -> 直引号
        text = re.sub(r'[＂"「」『』]', '"', text)
        # 右弯引号/全角右引号 -> 直引号
        text = re.sub(r'[＂"」』]', '"', text)
        return text
    

# 使用示例
if __name__ == "__main__":
    cleaner = TextCleaner()
    dirty_text = "<p>这是一段HTML文本，包含<a href='http://example.com'>链接</a>和 多余  空格。</p>"
    clean_text = cleaner.clean(dirty_text)
    print(f"清洗前: {dirty_text}")
    print(f"清洗后: {clean_text}")
