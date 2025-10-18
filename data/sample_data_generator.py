"""
Generate sample GDP data for demonstration purposes.
This script creates a sample dataset similar to the Kaggle World GDP Growth dataset.
"""

import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Countries to include
countries = [
    'United States', 'China', 'India', 'Japan', 'Germany', 
    'United Kingdom', 'France', 'Brazil', 'Italy', 'Canada',
    'South Korea', 'Russia', 'Spain', 'Australia', 'Mexico',
    'Indonesia', 'Netherlands', 'Saudi Arabia', 'Turkey', 'Switzerland',
    'Argentina', 'Poland', 'Thailand', 'Belgium', 'Sweden',
    'Nigeria', 'Austria', 'Singapore', 'Malaysia', 'Israel',
    'Hong Kong', 'Denmark', 'Philippines', 'Ireland', 'Pakistan',
    'Egypt', 'South Africa', 'Chile', 'Finland', 'Vietnam'
]

# Years
years = list(range(1980, 2025))

# Generate data
data = []

for country in countries:
    row = {'country_name': country, 'indicator_name': 'GDP growth (annual %)'}
    
    # Base growth rate varies by country
    if country in ['China', 'India', 'Vietnam', 'Indonesia']:
        base_growth = np.random.uniform(5, 8)
    elif country in ['United States', 'United Kingdom', 'Germany', 'Japan']:
        base_growth = np.random.uniform(1.5, 3)
    elif country in ['Brazil', 'Russia', 'South Africa', 'Argentina']:
        base_growth = np.random.uniform(1, 4)
    else:
        base_growth = np.random.uniform(2, 4)
    
    # Generate GDP growth for each year
    for i, year in enumerate(years):
        # Add trend and noise
        trend = 0
        
        # 2008-2009 financial crisis
        if year in [2008, 2009]:
            crisis_impact = np.random.uniform(-5, -2)
        else:
            crisis_impact = 0
        
        # 2020 COVID-19 pandemic
        if year == 2020:
            covid_impact = np.random.uniform(-8, -3)
        elif year == 2021:
            covid_impact = np.random.uniform(2, 6)  # Recovery
        else:
            covid_impact = 0
        
        # Random fluctuation
        noise = np.random.normal(0, 1.5)
        
        # Calculate final growth
        growth = base_growth + trend + crisis_impact + covid_impact + noise
        
        # Add some declining trend for developed countries
        if country in ['United States', 'Japan', 'Germany', 'United Kingdom']:
            growth -= (i / len(years)) * 0.5
        
        row[str(year)] = round(growth, 2)
    
    data.append(row)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_path = 'data/world_gdp_data.csv'
df.to_csv(output_path, index=False)

print(f"Sample data generated and saved to {output_path}")
print(f"Shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
