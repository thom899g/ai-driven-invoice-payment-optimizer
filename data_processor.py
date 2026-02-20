import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime

class DataProcessor:
    def __init__(self):
        self.cleaned_data = None
        self.validation_errors = []

    def _clean_data(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """Cleans and validates the input data."""
        try:
            df = pd.DataFrame(raw_data)
            # Convert date strings to datetime objects
            df['due_date'] = pd.to_datetime(df['due_date'])
            df['invoice_date'] = pd.to_datetime(df['invoice_date'])
            
            # Handle missing values
            df.dropna(inplace=True)
            
            return df
        except Exception as e:
            self.validation_errors.append(f"Data cleaning error: {str(e)}")
            raise

    def process_data(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """Processes and cleans the input data."""
        try:
            cleaned_df = self._clean_data(raw_data)
            
            # Validate data structure
            if 'invoice_id' not in cleaned_df.columns or \
               'amount' not in cleaned_df.columns:
                raise ValueError("Missing required columns")
            
            return cleaned_df
        except Exception as e:
            print(f"Error processing data: {str(e)}")
            raise

    def get_validation_errors(self) -> list:
        """Returns any validation errors encountered."""
        return self.validation_errors