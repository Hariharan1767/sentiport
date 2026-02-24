import numpy as np
import pandas as pd
from typing import Dict, Tuple
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from models import ModelFactory
from feature_engineering import MultiModalFeatureEngineer

class ResearchTrainingEngine:
    """
    Orchestrates the training and evaluation of baseline and hybrid models.
    """
    def __init__(self, window_size: int = 14):
        self.window_size = window_size
        self.factory = ModelFactory()
        
    def calculate_directional_accuracy(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculates whether the predicted movement direction matches actual."""
        # Note: We need the previous day's close to determine direction
        # Here we compare y[t] vs y[t-1]
        true_direction = np.diff(y_true) > 0
        pred_direction = np.diff(y_pred.flatten()) > 0
        return np.mean(true_direction == pred_direction)

    def evaluate_model(self, model, X_test, y_test, name: str) -> Dict:
        """Evaluates a model and returns a dictionary of metrics."""
        y_pred = model.predict(X_test)
        
        metrics = {
            "name": name,
            "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
            "mae": mean_absolute_error(y_test, y_pred),
            "r2": r2_score(y_test, y_pred),
            "directional_acc": self.calculate_directional_accuracy(y_test, y_pred)
        }
        return metrics

    def train_and_compare(self, Xp: np.ndarray, Xs: np.ndarray, y: np.ndarray, split_ratio: float = 0.8):
        """Trains both models and prints a comparative report."""
        split = int(len(Xp) * split_ratio)
        
        # Split Data
        Xp_train, Xp_test = Xp[:split], Xp[split:]
        Xs_train, Xs_test = Xs[:split], Xs[split:]
        y_train, y_test = y[:split], y[split:]
        
        # 1. Train Baseline
        print("\n--- Training Baseline Model ---")
        baseline = self.factory.build_baseline_lstm(Xp_train.shape[1:])
        baseline.fit(Xp_train, y_train, epochs=10, batch_size=32, verbose=0, validation_split=0.1)
        baseline_metrics = self.evaluate_model(baseline, Xp_test, y_test, "Baseline (Price Only)")
        
        # 2. Train Hybrid
        print("--- Training Hybrid Model ---")
        hybrid = self.factory.build_hybrid_model(Xp_train.shape[1:], Xs_train.shape[1])
        hybrid.fit([Xp_train, Xs_train], y_train, epochs=10, batch_size=32, verbose=0, validation_split=0.1)
        hybrid_metrics = self.evaluate_model(hybrid, [Xp_test, Xs_test], y_test, "Hybrid (Price + Sentiment)")
        
        return baseline_metrics, hybrid_metrics, (baseline, hybrid)

if __name__ == "__main__":
    # Mock data run
    engine = ResearchTrainingEngine(window_size=5)
    Xp = np.random.rand(100, 5, 7)
    Xs = np.random.rand(100, 3)
    y = np.random.rand(100)
    
    b_met, h_met, models = engine.train_and_compare(Xp, Xs, y)
    
    print("\nREPORT:")
    for m in [b_met, h_met]:
        print(f"{m['name']}: RMSE={m['rmse']:.4f}, DirAcc={m['directional_acc']:.2%}")
