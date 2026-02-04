"""
Return prediction module.
"""

import logging
import pandas as pd
import numpy as np
import joblib
from typing import Dict, List, Optional, Union
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from pathlib import Path

logger = logging.getLogger(__name__)

class ReturnPredictor:
    """
    Predicts future stock returns using trained models.
    """
    
    AVAILABLE_MODELS = {
        'random_forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
        'gradient_boosting': GradientBoostingRegressor(random_state=42),
        'linear_regression': LinearRegression(),
        'ridge': Ridge(alpha=1.0)
    }
    
    def __init__(self, model_type: str = 'random_forest'):
        if model_type not in self.AVAILABLE_MODELS:
            raise ValueError(f"Model type {model_type} not supported")
            
        self.model_type = model_type
        self.model = self.AVAILABLE_MODELS[model_type]
        self.feature_columns = []
        
    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> Dict[str, float]:
        """
        Train the model.
        """
        self.feature_columns = list(X_train.columns)
        logger.info(f"Training {self.model_type} on {len(X_train)} samples with {len(self.feature_columns)} features...")
        
        self.model.fit(X_train, y_train)
        
        # In-sample metrics
        y_pred = self.model.predict(X_train)
        rmse = np.sqrt(mean_squared_error(y_train, y_pred))
        return {'train_rmse': rmse}
        
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """
        Evaluate model performance.
        """
        y_pred = self.model.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Information Coefficient (Correlation between predicted and actual)
        ic = np.corrcoef(y_pred, y_test)[0, 1]
        
        # Directional Accuracy
        direction_match = (np.sign(y_pred) == np.sign(y_test)).mean()
        
        metrics = {
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'ic': ic,
            'directional_accuracy': direction_match
        }
        
        logger.info(f"Evaluation Metrics: {metrics}")
        return metrics
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Generate predictions.
        """
        # Ensure columns match training
        if self.feature_columns:
            X = X[self.feature_columns]
            
        return self.model.predict(X)
        
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance (if supported by model).
        """
        if hasattr(self.model, 'feature_importances_'):
            imps = self.model.feature_importances_
            return pd.DataFrame({
                'Feature': self.feature_columns,
                'Importance': imps
            }).sort_values('Importance', ascending=False)
        else:
            return pd.DataFrame()
            
    def save_model(self, filepath: str):
        joblib.dump({
            'model': self.model,
            'model_type': self.model_type,
            'features': self.feature_columns
        }, filepath)
        
    def load_model(self, filepath: str):
        data = joblib.load(filepath)
        self.model = data['model']
        self.model_type = data['model_type']
        self.feature_columns = data['features']
