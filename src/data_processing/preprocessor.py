"""
Text preprocessing pipeline: tokenization, lemmatization, stop word removal, etc.
"""
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class TextPreprocessor:
    """Text preprocessing class with complete NLP preprocessing pipeline"""
    
    def __init__(self, language: str = 'english'):
        """
        Initialize the preprocessor
        
        Args:
            language: Text language ('english', 'french', 'spanish', etc.)
        """
        self.language = language
        self.lemmatizer = WordNetLemmatizer()
        
        # Download necessary NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            logger.info("Downloading NLTK data...")
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
        
        # Get stop words list
        self.stop_words = set(stopwords.words(language))
        # Can add custom stop words
        self.custom_stopwords = {'said', 'would', 'could', 'also', 'like'}
        self.stop_words.update(self.custom_stopwords)
    
    def preprocess(self, text: str, 
                   remove_stopwords: bool = True,
                   lemmatize: bool = True,
                   min_word_length: int = 2) -> List[str]:
        """
        Preprocess a single text
        
        Args:
            text: Input text
            remove_stopwords: Whether to remove stop words
            lemmatize: Whether to perform lemmatization
            min_word_length: Minimum word length to keep
            
        Returns:
            List[str]: List of preprocessed tokens
        """
        if not text:
            return []
        
        # 1. Tokenization
        tokens = word_tokenize(text.lower())
        
        # 2. Remove punctuation and numbers (keep only letters)
        tokens = [token for token in tokens if token.isalpha()]
        
        # 3. Remove short words
        tokens = [token for token in tokens if len(token) >= min_word_length]
        
        # 4. Remove stop words
        if remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]
        
        # 5. Lemmatization
        if lemmatize:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return tokens
    
    def preprocess_batch(self, texts: List[str], **kwargs) -> List[List[str]]:
        """Batch preprocess texts"""
        return [self.preprocess(text, **kwargs) for text in texts]
    
    def get_preprocessed_text(self, text: str, **kwargs) -> str:
        """Return preprocessed string (not token list)"""
        tokens = self.preprocess(text, **kwargs)
        return ' '.join(tokens)
    

# Usage example
if __name__ == "__main__":
    preprocessor = TextPreprocessor(language='english')
    
    sample_text = "The quick brown foxes are jumping over the lazy dogs. They're having fun!"
    
    # Get token list
    tokens = preprocessor.preprocess(sample_text)
    print(f"Token list: {tokens}")
    
    # Get preprocessed text string
    processed_text = preprocessor.get_preprocessed_text(sample_text)
    print(f"Processed text: {processed_text}")
