"""
主题建模模块：支持LDA和BERTopic。
Topic Modeling Module: Supports LDA and BERTopic.
"""
from gensim import corpora, models
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TopicModeler:
    def __init__(self, method='bertopic'):
        self.method = method
        self.model = None
        self.topics = None
        
    def fit(self, documents):
        """训练主题模型"""
        if self.method == 'lda':
            # LDA实现
            texts = [doc.split() for doc in documents]
            dictionary = corpora.Dictionary(texts)
            corpus = [dictionary.doc2bow(text) for text in texts]
            self.model = models.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)
            self.topics = self.model.print_topics()
        elif self.method == 'bertopic':
            # BERTopic实现（文档未详述细节，但基于我所掌握的知识）
            sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
            embeddings = sentence_model.encode(documents, show_progress_bar=False)
            self.model = BERTopic(verbose=True)
            topics, _ = self.model.fit_transform(documents, embeddings)
            self.topics = self.model.get_topic_info()
        else:
            raise ValueError("Method must be 'lda' or 'bertopic'")
        logger.info(f"Model trained with {self.method}")
    
    def predict(self, new_documents):
        """预测新文档的主题"""
        if self.method == 'lda':
            # LDA预测逻辑
            pass
        else:
            topics, _ = self.model.transform(new_documents)
        return topics
