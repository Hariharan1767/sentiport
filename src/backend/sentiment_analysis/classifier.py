"""
Sentiment classification module using scikit-learn.
"""

import logging
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any, Union

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, f1_score

try:
    from textblob import TextBlob
    _TEXTBLOB_AVAILABLE = True
except ImportError:
    _TEXTBLOB_AVAILABLE = False

try:
    from preprocessing.text_cleaner import TextPreprocessor
except ImportError:
    TextPreprocessor = None

logger = logging.getLogger(__name__)


class SentimentClassifier:
    """
    Machine learning based sentiment classifier.
    
    Wraps scikit-learn pipeline with TfidfVectorizer and a classifier.
    Supports training, evaluation, and persistence.
    """
    
    AVAILABLE_MODELS = {
        'logistic_regression': LogisticRegression(max_iter=1000, random_state=42),
        'naive_bayes': MultinomialNB(),
        'linear_svc': LinearSVC(random_state=42, dual='auto')
    }
    
    def __init__(self, model_type: str = 'logistic_regression', 
                 max_features: int = 5000,
                 ngram_range: Tuple[int, int] = (1, 2)):
        """
        Initialize classifier.
        
        Args:
            model_type: One of 'logistic_regression', 'naive_bayes', 'linear_svc'
            max_features: Max features for TF-IDF
            ngram_range: N-gram range for TF-IDF
        """
        if model_type not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model type must be one of {list(self.AVAILABLE_MODELS.keys())}")
            
        self.model_type = model_type
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.pipeline = None
        self.best_params = None
        self.metrics = {}
        
        logger.info(f"Initialized SentimentClassifier (model={model_type})")

    def build_pipeline(self):
        """Build the scikit-learn pipeline."""
        classifier = self.AVAILABLE_MODELS[self.model_type]
        
        # Note: TextPreprocessor is not included in the pipeline here 
        # to allow saving just the model/vectorizer part, and assuming 
        # text is preprocessed beforehand or we can add it if needed.
        # For efficiency, we usually preprocess once before GridSearch.
        
        return Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=self.max_features,
                ngram_range=self.ngram_range,
                min_df=2,
                max_df=0.95
            )),
            ('clf', classifier)
        ])

    def train(self, X: Union[List[str], pd.Series], y: Union[List[int], pd.Series], 
              optimize: bool = True) -> Dict[str, float]:
        """
        Train the model.
        
        Args:
            X: List of text documents
            y: List of labels (-1, 0, 1)
            optimize: Whether to perform hyperparameter tuning
            
        Returns:
            Dictionary of evaluation metrics on training split (or validation split if optimizing)
        """
        logger.info(f"Training model on {len(X)} samples...")
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        pipeline = self.build_pipeline()
        
        if optimize and self.model_type == 'logistic_regression':
            logger.info("Performing hyperparameter tuning...")
            param_grid = {
                'tfidf__max_features': [3000, 5000],
                'clf__C': [0.1, 1.0, 10.0],
                'clf__class_weight': [None, 'balanced']
            }
            grid = GridSearchCV(
                pipeline, param_grid, cv=3, scoring='f1_weighted', n_jobs=-1, verbose=1
            )
            grid.fit(X_train, y_train)
            self.pipeline = grid.best_estimator_
            self.best_params = grid.best_params_
            logger.info(f"Best parameters: {self.best_params}")
        else:
            pipeline.fit(X_train, y_train)
            self.pipeline = pipeline
            
        # Evaluate on validation set
        y_pred = self.pipeline.predict(X_val)
        
        self.metrics = {
            'accuracy': accuracy_score(y_val, y_pred),
            'f1_weighted': f1_score(y_val, y_pred, average='weighted'),
            'f1_macro': f1_score(y_val, y_pred, average='macro')
        }
        
        logger.info(f"Validation Metrics: {self.metrics}")
        logger.info(f"\n{classification_report(y_val, y_pred)}")
        
        return self.metrics

    def predict(self, X: Union[List[str], pd.Series, str]) -> np.ndarray:
        """
        Predict sentiment.
        
        Args:
            X: Text(s) to classify
            
        Returns:
            Numpy array of labels
        """
        if self.pipeline is None:
            raise RuntimeError("Model not trained. Call train() or load_model() first.")
            
        if isinstance(X, str):
            X = [X]
            
        return self.pipeline.predict(X)
    
    def predict_proba(self, X: Union[List[str], pd.Series, str]) -> np.ndarray:
        """Predict class probabilities."""
        if self.pipeline is None:
            raise RuntimeError("Model not trained.")
            
        if isinstance(X, str):
            X = [X]
            
        if hasattr(self.pipeline, 'predict_proba'):
            return self.pipeline.predict_proba(X)
        elif hasattr(self.pipeline, 'decision_function'):
            # For LinearSVC, etc.
            return self.pipeline.decision_function(X)
        else:
            raise NotImplementedError("Model does not support probability/decision function")

    def save_model(self, filepath: str):
        """Save trained model."""
        if self.pipeline is None:
            raise RuntimeError("No model to save.")
            
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            'pipeline': self.pipeline,
            'model_type': self.model_type,
            'metrics': self.metrics,
            'best_params': self.best_params
        }, filepath)
        logger.info(f"Model saved to {filepath}")
        
    def load_model(self, filepath: str):
        """Load trained model."""
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
            
        data = joblib.load(filepath)
        self.pipeline = data['pipeline']
        self.model_type = data['model_type']
        self.metrics = data.get('metrics', {})
        self.best_params = data.get('best_params', {})
        
        logger.info(f"Model loaded from {filepath}")
        return self

    def predict_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Predict sentiment for a single text string.
        Used by api_server.py for quick per-article scoring.
        
        Returns:
            {'label': 'POSITIVE'|'NEUTRAL'|'NEGATIVE', 'score': float 0-1}
        
        Tries trained pipeline first; falls back to TextBlob if no model loaded.
        """
        if not text or not isinstance(text, str):
            return {'label': 'NEUTRAL', 'score': 0.5}
        
        # Try trained ML pipeline first
        if self.pipeline is not None:
            try:
                pred = self.pipeline.predict([text])[0]
                # Map label to score
                label_map = {1: 'POSITIVE', 0: 'NEUTRAL', -1: 'NEGATIVE',
                             'positive': 'POSITIVE', 'neutral': 'NEUTRAL', 'negative': 'NEGATIVE'}
                label = label_map.get(pred, 'NEUTRAL')
                score = 0.75 if label == 'POSITIVE' else 0.5 if label == 'NEUTRAL' else 0.25
                return {'label': label, 'score': score}
            except Exception:
                pass
        
        # Fallback: TextBlob polarity
        if _TEXTBLOB_AVAILABLE:
            try:
                polarity = TextBlob(text).sentiment.polarity  # -1 to 1
                score = (polarity + 1) / 2  # Normalise to 0-1
                if score > 0.6:
                    label = 'POSITIVE'
                elif score < 0.4:
                    label = 'NEGATIVE'
                else:
                    label = 'NEUTRAL'
                return {'label': label, 'score': round(score, 4)}
            except Exception:
                pass
        
        return {'label': 'NEUTRAL', 'score': 0.5}


if __name__ == "__main__":
    # Test run
    from data_collection.sentiment_data import SentimentDataPreparer
    
    # 1. Generate Data
    prep = SentimentDataPreparer()
    df = prep.create_sample_data(500)
    
    # 2. Preprocess
    cleaner = TextPreprocessor()
    df['clean_text'] = cleaner.transform(df['Headline'])
    
    # 3. Train
    clf = SentimentClassifier(model_type='logistic_regression')
    metrics = clf.train(df['clean_text'], df['Sentiment_Label'])
    
    # 4. Predict
    sample = ["Growth is skyrocketing!", "Sales are plummenting due to crisis."]
    sample_clean = cleaner.transform(sample)
    preds = clf.predict(sample_clean)
    print(f"Predictions for {sample}: {preds}")
