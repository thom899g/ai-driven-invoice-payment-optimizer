import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict, Any
import logging

class AIAgent:
    def __init__(self):
        self.model = LinearRegression()
        self._training_data = None
        self._target_column = 'predicted_delay_days'

    def _preprocess_data(self, data: pd.DataFrame) -> np.ndarray:
        """Preprocesses data for model input."""
        try:
            # Convert dates to ordinal day numbers
            features = data[['invoice_date', 'due_date']].apply(
                lambda x: (x['invoice_date'].toordinal(), 
                          x['due_date'].toordinal()))
            return np.array(features)
        except Exception as e:
            logging.error(f"Error preprocessing data: {str(e)}")
            raise

    def train_model(self, training_data: pd.DataFrame) -> None:
        """Trains the AI model."""
        try:
            features = self._preprocess_data(training_data)
            labels = training_data['delay_days'].values
            
            # Ensure labels are numeric
            if not np.issubdtype(labels.dtype, np.number):
                raise ValueError("Labels must be numeric")
            
            self.model.fit(features, labels)
            self._training_data = features
        except Exception as e:
            logging.error(f"Training failed: {str(e)}")
            raise

    def analyze_invoice(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes an invoice using the trained model."""
        try:
            # Preprocess new data point
            features = self._preprocess_data(pd.DataFrame([invoice_data]))
            
            # Make prediction
            prediction = self.model.predict(features)
            
            return {
                'predicted_delay': int(round(prediction[0], 0)),
                'risk_score': self._calculate_risk_score(invoice_data),
                'optimal_payment_term_days': self._suggest_optimal_terms(
                    invoice_data['amount'], prediction[0])
            }
        except Exception as e:
            logging.error(f"Analysis failed: {str(e)}")
            raise

    def _calculate_risk_score(self, amount: float, delay_days: int) -> float:
        """Calculates risk score based on amount and delay."""
        return (delay_days * 0.7) + ((amount / 1000000) * 0.3)

    def _suggest_optimal_terms(self, amount: float, delay_prediction: int) -> int:
        """Suggests optimal payment terms based on analysis."""
        if amount > 1000000 and delay_prediction > 30:
            return 60
        elif delay_prediction > 15:
            return 30
        else:
            return 15