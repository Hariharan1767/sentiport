import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Input, Concatenate, Dropout, Flatten
from typing import Tuple

class ModelFactory:
    """
    Creates various deep learning architectures for stock prediction.
    """
    
    @staticmethod
    def build_baseline_lstm(input_shape: Tuple[int, int]) -> Model:
        """
        Baseline LSTM model for price-only forecasting.
        input_shape: (window_size, feature_count)
        """
        inputs = Input(shape=input_shape)
        x = LSTM(64, return_sequences=True)(inputs)
        x = Dropout(0.2)(x)
        x = LSTM(32, return_sequences=False)(x)
        x = Dropout(0.2)(x)
        x = Dense(16, activation='relu')(x)
        outputs = Dense(1)(x)
        
        model = Model(inputs=inputs, outputs=outputs, name="Baseline_LSTM")
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    @staticmethod
    def build_hybrid_model(price_shape: Tuple[int, int], sentiment_shape: int) -> Model:
        """
        Hybrid Multi-Modal model combining temporal prices and static sentiment.
        price_shape: (window_size, price_feat_count)
        sentiment_shape: (sentiment_feat_count)
        """
        # Branch 1: Temporal Price Features
        price_inputs = Input(shape=price_shape, name="price_input")
        p = LSTM(64, return_sequences=True)(price_inputs)
        p = Dropout(0.2)(p)
        p = LSTM(32, return_sequences=False)(p)
        p = Dropout(0.2)(p)
        
        # Branch 2: Content/Sentiment Features
        sent_inputs = Input(shape=(sentiment_shape,), name="sentiment_input")
        s = Dense(16, activation='relu')(sent_inputs)
        s = Dense(8, activation='relu')(s)
        
        # Merge Branches
        merged = Concatenate()([p, s])
        
        # Output Layers
        m = Dense(16, activation='relu')(merged)
        outputs = Dense(1, name="prediction")(m)
        
        model = Model(inputs=[price_inputs, sent_inputs], outputs=outputs, name="Hybrid_MultiModal")
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

if __name__ == "__main__":
    # Test architectures
    factory = ModelFactory()
    
    baseline = factory.build_baseline_lstm((14, 7))
    baseline.summary()
    
    hybrid = factory.build_hybrid_model((14, 7), 3)
    hybrid.summary()
