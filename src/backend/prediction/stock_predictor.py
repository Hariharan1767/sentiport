
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator, ClassifierMixin

class StockPredictor(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def prepare_features(self, analysis_results):
        """
        Flattens the analysis results into a feature vector.
        """
        features = {}
        
        # Flatten scores
        features['fundamental_score'] = analysis_results['fundamental']['score']
        features['valuation_score'] = analysis_results['valuation']['score']
        features['growth_score'] = analysis_results['growth']['score']
        features['technical_score'] = analysis_results['technical']['score']
        features['risk_score'] = analysis_results['risk']['score']
        features['business_score'] = analysis_results['business']['score']
        features['management_score'] = analysis_results['management']['score']
        
        # Add raw metrics if needed normalization
        # For this prototype, we'll use the scores as high-level features
        
        return pd.DataFrame([features])

    def predict_invest_decision(self, analysis_results):
        """
        Predicts Invest (1) or No Invest (0) based on the comprehensive scorecard.
        Since we don't have a large labeled dataset for this specific 9-factor model yet,
        we will use a weighted heuristic that acts as a 'Knowledge-Based System'
        which mimics a pre-trained expert model.
        """
        
        # Weighted Ensemble (Expert System Approach)
        weights = {
            'fundamental': 2.0,  # Health is key
            'valuation': 1.5,    # Price matters
            'technical': 1.0,    # Timing
            'risk': 1.5,         # Risk management
            'growth': 1.5,       # Future
            'business': 1.0,     # Moat
            'management': 1.0    # Governance
        }
        
        scores = analysis_results
        
        total_score = (
            scores['fundamental']['score'] * weights['fundamental'] +
            scores['valuation']['score'] * weights['valuation'] +
            scores['growth']['score'] * weights['growth'] +
            scores['technical']['score'] * weights['technical'] +
            scores['risk']['score'] * weights['risk'] +
            scores['business']['score'] * weights['business'] +
            scores['management']['score'] * weights['management']
        )
        
        max_possible = (
            scores['fundamental']['max_score'] * weights['fundamental'] +
            scores['valuation']['max_score'] * weights['valuation'] +
            scores['growth']['max_score'] * weights['growth'] +
            scores['technical']['max_score'] * weights['technical'] +
            scores['risk']['max_score'] * weights['risk'] +
            scores['business']['max_score'] * weights['business'] +
            scores['management']['max_score'] * weights['management']
        )
        
        confidence = total_score / max_possible if max_possible > 0 else 0
        
        decision = "INVEST" if confidence > 0.60 else "WAIT/AVOID"
        
        return {
            "decision": decision,
            "confidence_score": confidence,
            "total_weighted_score": total_score,
            "max_possible_score": max_possible
        }
