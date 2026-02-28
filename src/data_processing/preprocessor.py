"""
文本预处理管道：分词、词形还原、去除停用词等。
"""
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class TextPreprocessor:
    """文本预处理类，包含完整NLP预处理流程"""
    
    def __init__(self, language: str = 'english'):
        """
        初始化预处理器
        
        参数:
            language: 文本语言 ('english', 'french', 'spanish'等)
        """
        self.language = language
        self.lemmatizer = WordNetLemmatizer()
        
        # 下载必要的NLTK数据
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            logger.info("下载NLTK数据...")
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
        
        # 获取停用词列表
        self.stop_words = set(stopwords.words(language))
        # 可添加自定义停用词
        self.custom_stopwords = {'said', 'would', 'could', 'also', 'like'}
        self.stop_words.update(self.custom_stopwords)
    
    def preprocess(self, text: str, 
                   remove_stopwords: bool = True,
                   lemmatize: bool = True,
                   min_word_length: int = 2) -> List[str]:
        """
        预处理单个文本
        
        参数:
            text: 输入文本
            remove_stopwords: 是否移除停用词
            lemmatize: 是否进行词形还原
            min_word_length: 保留的最小词长
            
        返回:
            List[str]: 预处理后的词元列表
        """
        if not text:
            return []
        
        # 1. 分词
        tokens = word_tokenize(text.lower())
        
        # 2. 移除标点符号和数字（只保留字母）
        tokens = [token for token in tokens if token.isalpha()]
        
        # 3. 移除短词
        tokens = [token for token in tokens if len(token) >= min_word_length]
        
        # 4. 移除停用词
        if remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words]
        
        # 5. 词形还原
        if lemmatize:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return tokens
    
    def preprocess_batch(self, texts: List[str], **kwargs) -> List[List[str]]:
        """批量预处理文本"""
        return [self.preprocess(text, **kwargs) for text in texts]
    
    def get_preprocessed_text(self, text: str, **kwargs) -> str:
        """返回预处理后的字符串（而非词元列表）"""
        tokens = self.preprocess(text, **kwargs)
        return ' '.join(tokens)
    

# 使用示例
if __name__ == "__main__":
    preprocessor = TextPreprocessor(language='english')
    
    sample_text = "The quick brown foxes are jumping over the lazy dogs. They're having fun!"
    
    # 获取词元列表
    tokens = preprocessor.preprocess(sample_text)
    print(f"词元列表: {tokens}")
    
    # 获取预处理后的文本字符串
    processed_text = preprocessor.get_preprocessed_text(sample_text)
    print(f"处理后的文本: {processed_text}")
