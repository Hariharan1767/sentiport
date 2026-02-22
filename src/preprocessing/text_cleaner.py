"""
Text preprocessing and cleaning module.
"""

import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin
import joblib
from pathlib import Path
import pandas as pd
from typing import List, Optional, Union

# Configure logging
logger = logging.getLogger(__name__)

# Download NLTK resources
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    logger.info("Downloading NLTK resources...")
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

class TextPreprocessor(BaseEstimator, TransformerMixin):
    """
    Text preprocessing pipeline compatible with scikit-learn.
    
    Features:
    - Lowercasing
    - URL/Email removal
    - Special character removal
    - Stopword removal
    - Lemmatization
    """
    
    def __init__(self, remove_stopwords: bool = True, lemmatize: bool = True):
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        
        self.stop_words = set(stopwords.words('english')) if remove_stopwords else set()
        self.lemmatizer = WordNetLemmatizer() if lemmatize else None
        
        logger.info(
            f"Initialized TextPreprocessor (stopwords={remove_stopwords}, "
            f"lemmatize={lemmatize})"
        )

    def clean_text(self, text: str) -> str:
        """
        Apply cleaning rules to a single text string.
        """
        if not isinstance(text, str):
            return ""

        # Lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove emails
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove numbers and special characters (keep words only)
        # text = re.sub(r'[^a-zA-Z\s]', '', text) 
        # Better to keep some punctuation? No, standard bag-of-words usually removes it.
        text = re.sub(r'[^a-z\s]', ' ', text) # Replace non-letters with space
        
        # Tokenize (simple split)
        tokens = text.split()
        
        # Remove stopwords
        if self.remove_stopwords:
            tokens = [t for t in tokens if t not in self.stop_words]
            
        # Lemmatize
        if self.lemmatize:
            tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
            
        # Remove short words (optional, < 2 chars)
        tokens = [t for t in tokens if len(t) > 1]
        
        return ' '.join(tokens)

    def fit(self, X, y=None):
        """No-op, as this preprocessor is stateless."""
        return self

    def transform(self, X: Union[List[str], pd.Series]) -> List[str]:
        """
        Transform a list/series of texts.
        """
        if hasattr(X, 'tolist'): # pandas Series
            X = X.tolist()
            
        logger.info(f"Preprocessing {len(X)} texts...")
        return [self.clean_text(text) for text in X]
        
    def save(self, filepath: str):
        """Save preprocessor configuration."""
        joblib.dump(self, filepath)
        logger.info(f"TextPreprocessor saved to {filepath}")
        
    @classmethod
    def load(cls, filepath: str):
        """Load preprocessor configuration."""
        logger.info(f"Loading TextPreprocessor from {filepath}")
        return joblib.load(filepath)

if __name__ == "__main__":
    # Test run
    import pandas as pd
    
    examples = [
        "Apple's stock hit a new record high of $150! https://finance.yahoo.com",
        "Market crash: Investors panic as generic_email@example.com reports losses.",
        "The quick brown fox jumps over 123 lazy dogs."
    ]
    
    preprocessor = TextPreprocessor()
    processed = preprocessor.transform(examples)
    
    for orig, clean in zip(examples, processed):
        print(f"Original: {orig}")
        print(f"Cleaned:  {clean}")
        print("-" * 50)
