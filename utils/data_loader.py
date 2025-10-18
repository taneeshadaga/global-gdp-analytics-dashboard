"""
Data loading and preprocessing utilities for GDP analytics dashboard.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


# Regional mapping for countries
COUNTRY_REGION_MAPPING = {
    'United States': 'North America',
    'Canada': 'North America',
    'Mexico': 'North America',
    'Brazil': 'South America',
    'Argentina': 'South America',
    'Chile': 'South America',
    'Colombia': 'South America',
    'Peru': 'South America',
    'United Kingdom': 'Europe',
    'Germany': 'Europe',
    'France': 'Europe',
    'Italy': 'Europe',
    'Spain': 'Europe',
    'Netherlands': 'Europe',
    'Belgium': 'Europe',
    'Sweden': 'Europe',
    'Switzerland': 'Europe',
    'Poland': 'Europe',
    'Russia': 'Europe',
    'China': 'Asia',
    'India': 'Asia',
    'Japan': 'Asia',
    'South Korea': 'Asia',
    'Indonesia': 'Asia',
    'Thailand': 'Asia',
    'Vietnam': 'Asia',
    'Singapore': 'Asia',
    'Malaysia': 'Asia',
    'Philippines': 'Asia',
    'Pakistan': 'Asia',
    'Bangladesh': 'Asia',
    'Australia': 'Oceania',
    'New Zealand': 'Oceania',
    'South Africa': 'Africa',
    'Nigeria': 'Africa',
    'Egypt': 'Africa',
    'Kenya': 'Africa',
    'Ghana': 'Africa',
    'Ethiopia': 'Africa',
    'Saudi Arabia': 'Middle East',
    'United Arab Emirates': 'Middle East',
    'Israel': 'Middle East',
    'Turkey': 'Middle East',
    'Iran': 'Middle East',
}


def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Load GDP data and convert from wide to long format.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Cleaned DataFrame in long format
    """
    # Load data - try multiple encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if df is None:
        raise ValueError(f"Could not read file {file_path} with any of the attempted encodings: {encodings}")
    
    # Get year columns (all columns that are numeric years)
    year_cols = [col for col in df.columns if col.isdigit() and 1980 <= int(col) <= 2024]
    
    # Melt from wide to long format
    id_vars = ['country_name', 'indicator_name'] if 'indicator_name' in df.columns else ['country_name']
    
    df_long = df.melt(
        id_vars=id_vars,
        value_vars=year_cols,
        var_name='year',
        value_name='gdp_growth'
    )
    
    # Clean data
    df_long['year'] = df_long['year'].astype(int)
    df_long['gdp_growth'] = pd.to_numeric(df_long['gdp_growth'], errors='coerce')
    
    # Add regional grouping
    df_long['region'] = df_long['country_name'].map(COUNTRY_REGION_MAPPING)
    df_long['region'] = df_long['region'].fillna('Other')
    
    # Remove rows with missing GDP growth
    df_long = df_long.dropna(subset=['gdp_growth'])
    
    # Sort by country and year
    df_long = df_long.sort_values(['country_name', 'year']).reset_index(drop=True)
    
    return df_long


def get_country_data(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Extract data for a specific country.
    
    Args:
        df: Full DataFrame
        country: Country name
        
    Returns:
        Country-specific DataFrame
    """
    return df[df['country_name'] == country].copy()


def get_regional_data(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Extract data for a specific region.
    
    Args:
        df: Full DataFrame
        region: Region name
        
    Returns:
        Region-specific DataFrame
    """
    return df[df['region'] == region].copy()


def calculate_summary_stats(df: pd.DataFrame) -> Dict:
    """
    Calculate summary statistics for the dataset.
    
    Args:
        df: DataFrame with GDP data
        
    Returns:
        Dictionary of summary statistics
    """
    stats = {
        'avg_growth': df['gdp_growth'].mean(),
        'median_growth': df['gdp_growth'].median(),
        'std_growth': df['gdp_growth'].std(),
        'min_growth': df['gdp_growth'].min(),
        'max_growth': df['gdp_growth'].max(),
        'num_countries': df['country_name'].nunique(),
        'num_years': df['year'].nunique(),
        'total_observations': len(df)
    }
    
    return stats


def get_top_performers(df: pd.DataFrame, n: int = 10, year_range: Tuple[int, int] = None) -> pd.DataFrame:
    """
    Get top performing countries by average GDP growth.
    
    Args:
        df: DataFrame with GDP data
        n: Number of top performers to return
        year_range: Optional tuple of (start_year, end_year)
        
    Returns:
        DataFrame of top performers
    """
    if year_range:
        df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    top = df.groupby('country_name')['gdp_growth'].mean().sort_values(ascending=False).head(n)
    
    return pd.DataFrame({
        'country': top.index,
        'avg_gdp_growth': top.values
    })


def get_bottom_performers(df: pd.DataFrame, n: int = 10, year_range: Tuple[int, int] = None) -> pd.DataFrame:
    """
    Get bottom performing countries by average GDP growth.
    
    Args:
        df: DataFrame with GDP data
        n: Number of bottom performers to return
        year_range: Optional tuple of (start_year, end_year)
        
    Returns:
        DataFrame of bottom performers
    """
    if year_range:
        df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    bottom = df.groupby('country_name')['gdp_growth'].mean().sort_values(ascending=True).head(n)
    
    return pd.DataFrame({
        'country': bottom.index,
        'avg_gdp_growth': bottom.values
    })


def detect_recessions(df: pd.DataFrame, threshold: float = -2.0) -> pd.DataFrame:
    """
    Detect recession periods (negative GDP growth).
    
    Args:
        df: DataFrame with GDP data
        threshold: GDP growth threshold to define recession
        
    Returns:
        DataFrame of recession periods
    """
    recessions = df[df['gdp_growth'] < threshold].copy()
    recessions = recessions.sort_values('gdp_growth').reset_index(drop=True)
    
    return recessions


def calculate_volatility(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """
    Calculate GDP growth volatility (rolling standard deviation).
    
    Args:
        df: DataFrame with GDP data
        window: Rolling window size
        
    Returns:
        DataFrame with volatility metrics
    """
    volatility_data = []
    
    for country in df['country_name'].unique():
        country_df = df[df['country_name'] == country].sort_values('year')
        country_df['volatility'] = country_df['gdp_growth'].rolling(window=window).std()
        volatility_data.append(country_df)
    
    return pd.concat(volatility_data, ignore_index=True)


def prepare_ml_data(df: pd.DataFrame, country: str) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Prepare data for machine learning models.
    
    Args:
        df: Full DataFrame
        country: Country name
        
    Returns:
        Tuple of (country_df, X, y) for modeling
    """
    country_df = get_country_data(df, country)
    country_df = country_df.sort_values('year').reset_index(drop=True)
    
    # Create features
    X = country_df['year'].values.reshape(-1, 1)
    y = country_df['gdp_growth'].values
    
    return country_df, X, y
