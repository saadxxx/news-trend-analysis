"""
Text cleaning module: Process raw text, remove irrelevant characters, standardize format.
"""
import re
import html
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class TextCleaner:
    """Class for cleaning news text"""
    
    def __init__(self, remove_patterns: Optional[list] = None):
        """
        Initialize the cleaner
        
        Args:
            remove_patterns: Custom regex pattern list for removing specific text
        """
        # Default cleaning patterns: HTML tags, URLs, emails, special symbols, extra whitespace
        self.default_patterns = [
            r'<[^>]+>',  # HTML tags
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URLs
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email addresses
            r'[^\w\s.,!?;:\'\"-]',  # Unusual symbols (keep basic punctuation)
            r'\s+',  # Multiple whitespace characters
        ]
        
        self.patterns = self.default_patterns + (remove_patterns or [])
    
    def clean(self, text: str) -> str:
        """
        Execute complete text cleaning process
        
        Args:
            text: Raw text string
            
        Returns:
            str: Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        cleaned = text
        
        # 1. Decode HTML entities (e.g., &amp; -> &)
        cleaned = html.unescape(cleaned)
        
        # 2. Remove all matched pattern content
        for pattern in self.patterns:
            cleaned = re.sub(pattern, ' ', cleaned)
        
        # 3. Standardize whitespace characters (multiple spaces/newlines to single space)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # 4. Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        
        # 5. Normalize quotes (optional, for multilingual text)
        cleaned = self._normalize_quotes(cleaned)
        
        logger.debug(f"Text cleaning completed: Original length {len(text)}, Cleaned length {len(cleaned)}")
        return cleaned
    
    def clean_batch(self, texts: list) -> list:
        """Batch clean text list"""
        return [self.clean(text) for text in texts]
    
    def _normalize_quotes(self, text: str) -> str:
        """Normalize curly quotes, full-width quotes, etc. to straight quotes"""
        # Left curly quotes/full-width left quotes -> straight quotes
        text = re.sub(r'[＂"「」『』]', '"', text)
        # Right curly quotes/full-width right quotes -> straight quotes
        text = re.sub(r'[＂"」』]', '"', text)
        return text
    

# Usage example
if __name__ == "__main__":
    cleaner = TextCleaner()
    dirty_text = "<p>This is HTML text containing <a href='http://example.com'>link</a> and extra   spaces.</p>"
    clean_text = cleaner.clean(dirty_text)
    print(f"Before cleaning: {dirty_text}")
    print(f"After cleaning: {clean_text}")
