"""
Machine Learning forecasting models for GDP growth prediction.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict
import warnings
warnings.filterwarnings('ignore')

from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


class ARIMAForecaster:
    """ARIMA-based GDP growth forecaster."""
    
    def __init__(self, order: Tuple[int, int, int] = (2, 1, 2)):
        """
        Initialize ARIMA forecaster.
        
        Args:
            order: ARIMA order (p, d, q)
        """
        self.order = order
        self.model = None
        self.model_fit = None
        
    def fit(self, y: np.ndarray) -> None:
        """
        Fit ARIMA model to data.
        
        Args:
            y: Time series data
        """
        self.model = ARIMA(y, order=self.order)
        self.model_fit = self.model.fit()
        
    def predict(self, steps: int = 10) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Make predictions with confidence intervals.
        
        Args:
            steps: Number of steps to forecast
            
        Returns:
            Tuple of (forecast, lower_bound, upper_bound)
        """
        forecast_result = self.model_fit.get_forecast(steps=steps)
        forecast = forecast_result.predicted_mean
        conf_int = forecast_result.conf_int()
        
        return forecast, conf_int[:, 0], conf_int[:, 1]
    
    def get_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        Calculate model performance metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary of metrics
        """
        return {
            'MAE': mean_absolute_error(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'R2': r2_score(y_true, y_pred)
        }


class ProphetForecaster:
    """Prophet-based GDP growth forecaster."""
    
    def __init__(self):
        """Initialize Prophet forecaster."""
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            interval_width=0.95
        )
        
    def fit(self, df: pd.DataFrame) -> None:
        """
        Fit Prophet model to data.
        
        Args:
            df: DataFrame with 'year' and 'gdp_growth' columns
        """
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        prophet_df = pd.DataFrame({
            'ds': pd.to_datetime(df['year'].astype(str) + '-01-01'),
            'y': df['gdp_growth']
        })
        
        self.model.fit(prophet_df)
        
    def predict(self, years: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Make predictions with confidence intervals.
        
        Args:
            years: Array of years to forecast
            
        Returns:
            Tuple of (forecast, lower_bound, upper_bound)
        """
        future = pd.DataFrame({
            'ds': pd.to_datetime(years.astype(str) + '-01-01')
        })
        
        forecast = self.model.predict(future)
        
        return forecast['yhat'].values, forecast['yhat_lower'].values, forecast['yhat_upper'].values
    
    def get_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        Calculate model performance metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary of metrics
        """
        return {
            'MAE': mean_absolute_error(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'R2': r2_score(y_true, y_pred)
        }


class XGBoostForecaster:
    """XGBoost-based GDP growth forecaster."""
    
    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1):
        """
        Initialize XGBoost forecaster.
        
        Args:
            n_estimators: Number of boosting rounds
            learning_rate: Learning rate
        """
        self.model = XGBRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=5,
            random_state=42,
            objective='reg:squarederror'
        )
        self.feature_cols = None
        
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create time-based features for XGBoost.
        
        Args:
            df: DataFrame with 'year' column
            
        Returns:
            DataFrame with engineered features
        """
        df = df.copy()
        df['year_idx'] = df['year'] - df['year'].min()
        df['year_squared'] = df['year_idx'] ** 2
        
        # Lag features
        df['lag_1'] = df['gdp_growth'].shift(1)
        df['lag_2'] = df['gdp_growth'].shift(2)
        df['lag_3'] = df['gdp_growth'].shift(3)
        
        # Rolling statistics
        df['rolling_mean_3'] = df['gdp_growth'].rolling(window=3, min_periods=1).mean()
        df['rolling_std_3'] = df['gdp_growth'].rolling(window=3, min_periods=1).std()
        
        return df
    
    def fit(self, df: pd.DataFrame) -> None:
        """
        Fit XGBoost model to data.
        
        Args:
            df: DataFrame with 'year' and 'gdp_growth' columns
        """
        df_features = self.create_features(df)
        df_features = df_features.dropna()
        
        self.feature_cols = ['year_idx', 'year_squared', 'lag_1', 'lag_2', 'lag_3', 
                            'rolling_mean_3', 'rolling_std_3']
        
        X = df_features[self.feature_cols]
        y = df_features['gdp_growth']
        
        self.model.fit(X, y)
        self.last_data = df.tail(5).copy()
        
    def predict(self, df: pd.DataFrame, future_years: np.ndarray) -> np.ndarray:
        """
        Make predictions for future years.
        
        Args:
            df: Historical DataFrame
            future_years: Array of years to forecast
            
        Returns:
            Array of predictions
        """
        predictions = []
        current_df = df.copy()
        
        for year in future_years:
            # Create a new row for the future year
            new_row = pd.DataFrame({
                'year': [year],
                'gdp_growth': [np.nan]  # Will be predicted
            })
            
            temp_df = pd.concat([current_df, new_row], ignore_index=True)
            temp_df_features = self.create_features(temp_df)
            
            # Get the last row features
            last_row = temp_df_features.iloc[-1:][self.feature_cols]
            
            # Handle NaN values by forward filling
            last_row = last_row.fillna(method='ffill').fillna(method='bfill').fillna(0)
            
            # Make prediction
            pred = self.model.predict(last_row)[0]
            predictions.append(pred)
            
            # Update the dataframe with the prediction
            current_df = pd.concat([current_df, pd.DataFrame({
                'year': [year],
                'gdp_growth': [pred]
            })], ignore_index=True)
        
        return np.array(predictions)
    
    def get_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        Calculate model performance metrics.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary of metrics
        """
        return {
            'MAE': mean_absolute_error(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'R2': r2_score(y_true, y_pred)
        }


def compare_models(df: pd.DataFrame, test_size: float = 0.2) -> Dict:
    """
    Compare performance of different forecasting models.
    
    Args:
        df: DataFrame with 'year' and 'gdp_growth' columns
        test_size: Proportion of data to use for testing
        
    Returns:
        Dictionary of model comparisons
    """
    # Split data
    split_idx = int(len(df) * (1 - test_size))
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    results = {}
    
    # ARIMA
    try:
        arima = ARIMAForecaster(order=(2, 1, 2))
        arima.fit(train_df['gdp_growth'].values)
        arima_pred, _, _ = arima.predict(steps=len(test_df))
        results['ARIMA'] = arima.get_metrics(test_df['gdp_growth'].values, arima_pred)
    except Exception as e:
        results['ARIMA'] = {'error': str(e)}
    
    # Prophet
    try:
        prophet = ProphetForecaster()
        prophet.fit(train_df)
        prophet_pred, _, _ = prophet.predict(test_df['year'].values)
        results['Prophet'] = prophet.get_metrics(test_df['gdp_growth'].values, prophet_pred)
    except Exception as e:
        results['Prophet'] = {'error': str(e)}
    
    # XGBoost
    try:
        xgb = XGBoostForecaster()
        xgb.fit(train_df)
        xgb_pred = xgb.predict(train_df, test_df['year'].values)
        results['XGBoost'] = xgb.get_metrics(test_df['gdp_growth'].values, xgb_pred)
    except Exception as e:
        results['XGBoost'] = {'error': str(e)}
    
    return results
