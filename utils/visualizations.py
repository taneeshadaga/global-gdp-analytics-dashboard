"""
Interactive visualization utilities using Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict


def create_time_series_plot(
    df: pd.DataFrame,
    countries: List[str],
    title: str = "GDP Growth Over Time"
) -> go.Figure:
    """
    Create interactive time series plot for selected countries.
    
    Args:
        df: DataFrame with GDP data
        countries: List of countries to plot
        title: Plot title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    for country in countries:
        country_data = df[df['country_name'] == country]
        fig.add_trace(go.Scatter(
            x=country_data['year'],
            y=country_data['gdp_growth'],
            mode='lines+markers',
            name=country,
            hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>GDP Growth: %{y:.2f}%<extra></extra>'
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="GDP Growth (%)",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig


def create_regional_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Create regional comparison box plot.
    
    Args:
        df: DataFrame with GDP data
        
    Returns:
        Plotly figure
    """
    fig = px.box(
        df,
        x='region',
        y='gdp_growth',
        color='region',
        title='GDP Growth Distribution by Region',
        labels={'gdp_growth': 'GDP Growth (%)', 'region': 'Region'}
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    return fig


def create_top_performers_bar(df: pd.DataFrame, n: int = 10) -> go.Figure:
    """
    Create bar chart of top performing countries.
    
    Args:
        df: DataFrame with country and avg_gdp_growth columns
        n: Number of countries to show
        
    Returns:
        Plotly figure
    """
    fig = px.bar(
        df.head(n),
        x='avg_gdp_growth',
        y='country',
        orientation='h',
        title=f'Top {n} Countries by Average GDP Growth',
        labels={'avg_gdp_growth': 'Average GDP Growth (%)', 'country': 'Country'},
        color='avg_gdp_growth',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def create_correlation_heatmap(df: pd.DataFrame, regions: List[str]) -> go.Figure:
    """
    Create correlation heatmap between regions over time.
    
    Args:
        df: DataFrame with GDP data
        regions: List of regions to include
        
    Returns:
        Plotly figure
    """
    # Pivot to get regions as columns
    pivot_df = df[df['region'].isin(regions)].pivot_table(
        index='year',
        columns='region',
        values='gdp_growth',
        aggfunc='mean'
    )
    
    # Calculate correlation
    corr_matrix = pivot_df.corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='GDP Growth Correlation Between Regions',
        template='plotly_white',
        height=500
    )
    
    return fig


def create_forecast_plot(
    historical_df: pd.DataFrame,
    forecast_years: np.ndarray,
    forecast_values: np.ndarray,
    lower_bound: np.ndarray = None,
    upper_bound: np.ndarray = None,
    title: str = "GDP Growth Forecast"
) -> go.Figure:
    """
    Create forecast plot with confidence intervals.
    
    Args:
        historical_df: Historical data DataFrame
        forecast_years: Array of forecast years
        forecast_values: Array of forecast values
        lower_bound: Lower confidence bound
        upper_bound: Upper confidence bound
        title: Plot title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=historical_df['year'],
        y=historical_df['gdp_growth'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='blue'),
        hovertemplate='Year: %{x}<br>GDP Growth: %{y:.2f}%<extra></extra>'
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_years,
        y=forecast_values,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='red', dash='dash'),
        hovertemplate='Year: %{x}<br>Forecast: %{y:.2f}%<extra></extra>'
    ))
    
    # Confidence interval
    if lower_bound is not None and upper_bound is not None:
        fig.add_trace(go.Scatter(
            x=np.concatenate([forecast_years, forecast_years[::-1]]),
            y=np.concatenate([upper_bound, lower_bound[::-1]]),
            fill='toself',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(color='rgba(255,0,0,0)'),
            name='95% Confidence Interval',
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="GDP Growth (%)",
        template='plotly_white',
        height=500,
        hovermode='x unified'
    )
    
    return fig


def create_policy_comparison_plot(scenarios_df: pd.DataFrame) -> go.Figure:
    """
    Create comparison plot for different policy scenarios.
    
    Args:
        scenarios_df: DataFrame with scenario results
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Baseline
    fig.add_trace(go.Bar(
        x=scenarios_df['scenario'],
        y=scenarios_df['baseline_growth'],
        name='Baseline Growth',
        marker_color='lightblue',
        hovertemplate='Baseline: %{y:.2f}%<extra></extra>'
    ))
    
    # Policy-adjusted
    fig.add_trace(go.Bar(
        x=scenarios_df['scenario'],
        y=scenarios_df['projected_growth'],
        name='Policy-Adjusted Growth',
        marker_color='coral',
        hovertemplate='Projected: %{y:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title='GDP Growth: Baseline vs. Policy Scenarios',
        xaxis_title='Scenario',
        yaxis_title='GDP Growth (%)',
        barmode='group',
        template='plotly_white',
        height=500
    )
    
    return fig


def create_impact_waterfall(impact_data: Dict) -> go.Figure:
    """
    Create waterfall chart showing policy impact breakdown.
    
    Args:
        impact_data: Dictionary with impact breakdown
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(go.Waterfall(
        name="Impact",
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=["Baseline Growth", "Direct Impact", "Multiplier Effect", "New Growth"],
        y=[
            impact_data['baseline_growth'],
            impact_data['direct_impact'],
            impact_data['multiplier_effect'],
            impact_data['new_growth']
        ],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title="Policy Impact Breakdown",
        yaxis_title="GDP Growth (%)",
        template='plotly_white',
        height=500
    )
    
    return fig


def create_world_map(df: pd.DataFrame, year: int) -> go.Figure:
    """
    Create choropleth world map of GDP growth.
    
    Args:
        df: DataFrame with GDP data
        year: Year to display
        
    Returns:
        Plotly figure
    """
    year_data = df[df['year'] == year].copy()
    
    fig = px.choropleth(
        year_data,
        locations='country_name',
        locationmode='country names',
        color='gdp_growth',
        hover_name='country_name',
        hover_data={'gdp_growth': ':.2f'},
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        title=f'Global GDP Growth - {year}',
        labels={'gdp_growth': 'GDP Growth (%)'}
    )
    
    fig.update_layout(
        template='plotly_white',
        height=600
    )
    
    return fig


def create_volatility_plot(df: pd.DataFrame, countries: List[str]) -> go.Figure:
    """
    Create volatility plot for selected countries.
    
    Args:
        df: DataFrame with volatility data
        countries: List of countries to plot
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    for country in countries:
        country_data = df[df['country_name'] == country].dropna(subset=['volatility'])
        fig.add_trace(go.Scatter(
            x=country_data['year'],
            y=country_data['volatility'],
            mode='lines',
            name=country,
            hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Volatility: %{y:.2f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='GDP Growth Volatility Over Time',
        xaxis_title='Year',
        yaxis_title='Volatility (Rolling Std Dev)',
        template='plotly_white',
        height=500,
        hovermode='x unified'
    )
    
    return fig


def create_scatter_matrix(df: pd.DataFrame, year_range: tuple) -> go.Figure:
    """
    Create scatter matrix for multi-dimensional analysis.
    
    Args:
        df: DataFrame with GDP data
        year_range: Tuple of (start_year, end_year)
        
    Returns:
        Plotly figure
    """
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    # Aggregate data
    agg_df = filtered_df.groupby('country_name').agg({
        'gdp_growth': ['mean', 'std', 'min', 'max']
    }).reset_index()
    
    agg_df.columns = ['country', 'avg_growth', 'volatility', 'min_growth', 'max_growth']
    
    fig = px.scatter_matrix(
        agg_df,
        dimensions=['avg_growth', 'volatility', 'min_growth', 'max_growth'],
        title=f'GDP Growth Characteristics ({year_range[0]}-{year_range[1]})',
        height=700
    )
    
    fig.update_layout(template='plotly_white')
    
    return fig
