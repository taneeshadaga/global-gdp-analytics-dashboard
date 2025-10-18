"""
AI-powered insights generation using LLM (optional feature).
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import os


def generate_statistical_insights(df: pd.DataFrame, stats: Dict) -> str:
    """
    Generate statistical insights without using external AI.
    
    Args:
        df: DataFrame with GDP data
        stats: Dictionary of summary statistics
        
    Returns:
        Formatted insights text
    """
    insights = []
    
    # Global trends
    insights.append("📊 **GLOBAL GDP GROWTH INSIGHTS**\n")
    
    insights.append(f"**Overall Performance:**")
    insights.append(f"• Average global GDP growth: {stats['avg_growth']:.2f}%")
    insights.append(f"• Median growth: {stats['median_growth']:.2f}%")
    insights.append(f"• Standard deviation: {stats['std_growth']:.2f}%")
    insights.append(f"• Coverage: {stats['num_countries']} countries over {stats['num_years']} years\n")
    
    # Identify periods
    yearly_avg = df.groupby('year')['gdp_growth'].mean()
    best_year = yearly_avg.idxmax()
    worst_year = yearly_avg.idxmin()
    
    insights.append(f"**Key Historical Periods:**")
    insights.append(f"• Best year: {best_year} ({yearly_avg[best_year]:.2f}% average growth)")
    insights.append(f"• Worst year: {worst_year} ({yearly_avg[worst_year]:.2f}% average growth)")
    
    # Recent trend
    recent_years = df[df['year'] >= 2020]
    if len(recent_years) > 0:
        recent_avg = recent_years['gdp_growth'].mean()
        insights.append(f"• Recent period (2020+): {recent_avg:.2f}% average growth\n")
    
    # Regional insights
    regional_avg = df.groupby('region')['gdp_growth'].mean().sort_values(ascending=False)
    insights.append(f"**Regional Performance:**")
    for region, avg in regional_avg.head(3).items():
        insights.append(f"• {region}: {avg:.2f}% average growth")
    
    return "\n".join(insights)


def generate_forecast_insights(
    country: str,
    historical_avg: float,
    forecast_avg: float,
    model_name: str
) -> str:
    """
    Generate insights about forecast results.
    
    Args:
        country: Country name
        historical_avg: Historical average growth
        forecast_avg: Forecasted average growth
        model_name: Name of forecasting model
        
    Returns:
        Formatted insights text
    """
    insights = []
    
    insights.append(f"📈 **FORECAST INSIGHTS FOR {country.upper()}**\n")
    
    insights.append(f"**Model Used:** {model_name}\n")
    
    insights.append(f"**Performance Comparison:**")
    insights.append(f"• Historical average: {historical_avg:.2f}%")
    insights.append(f"• Forecasted average: {forecast_avg:.2f}%")
    
    change = forecast_avg - historical_avg
    change_pct = (change / historical_avg * 100) if historical_avg != 0 else 0
    
    if abs(change) < 0.5:
        trend = "remain relatively stable"
    elif change > 0:
        trend = f"increase by {change:.2f}pp ({abs(change_pct):.1f}%)"
    else:
        trend = f"decrease by {abs(change):.2f}pp ({abs(change_pct):.1f}%)"
    
    insights.append(f"• Expected change: GDP growth is projected to {trend}\n")
    
    # Interpretation
    insights.append(f"**Interpretation:**")
    if forecast_avg > 3.0:
        insights.append(f"• Strong growth expected - {country} shows robust economic prospects")
    elif forecast_avg > 1.5:
        insights.append(f"• Moderate growth expected - stable economic trajectory")
    elif forecast_avg > 0:
        insights.append(f"• Slow growth expected - economy may face headwinds")
    else:
        insights.append(f"• Contraction risk - economic challenges ahead")
    
    return "\n".join(insights)


def generate_policy_insights(
    country: str,
    impact_data: Dict,
    tariff_change: float
) -> str:
    """
    Generate insights about policy simulation results.
    
    Args:
        country: Country name
        impact_data: Dictionary with impact analysis
        tariff_change: Tariff change amount
        
    Returns:
        Formatted insights text
    """
    insights = []
    
    insights.append(f"🏛️ **POLICY IMPACT INSIGHTS FOR {country.upper()}**\n")
    
    insights.append(f"**Scenario:** {'+' if tariff_change > 0 else ''}{tariff_change}% tariff change\n")
    
    insights.append(f"**Economic Impact:**")
    insights.append(f"• Direct effect: {impact_data['direct_impact']:.3f}pp")
    insights.append(f"• Multiplier effect: {impact_data['multiplier_effect']:.3f}pp")
    insights.append(f"• Total impact: {impact_data['total_impact']:.3f}pp")
    insights.append(f"• New growth rate: {impact_data['new_growth']:.2f}%\n")
    
    # Recommendations
    insights.append(f"**Policy Recommendations:**")
    
    if tariff_change > 0:
        if impact_data['total_impact'] < -0.5:
            insights.append(f"⚠️ **High Risk:** This tariff increase could significantly harm economic growth")
            insights.append(f"• Consider: Gradual implementation or targeted exemptions")
            insights.append(f"• Monitor: Trade partner retaliation risks")
        else:
            insights.append(f"⚡ **Moderate Risk:** Some economic slowdown expected")
            insights.append(f"• Consider: Balancing trade protection with growth objectives")
    else:
        if impact_data['total_impact'] > 0.5:
            insights.append(f"✅ **Positive Outlook:** Tariff reduction could boost growth")
            insights.append(f"• Opportunity: Enhanced trade competitiveness")
            insights.append(f"• Consider: Complementary pro-trade policies")
    
    return "\n".join(insights)


def generate_openai_insights(
    data_summary: str,
    api_key: str = None
) -> str:
    """
    Generate AI insights using OpenAI GPT (requires API key).
    
    Args:
        data_summary: Summary of data to analyze
        api_key: OpenAI API key
        
    Returns:
        AI-generated insights
    """
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        return "⚠️ OpenAI API key not configured. Using statistical insights instead."
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        prompt = f"""You are an expert economist analyzing global GDP growth data. 
        
Based on the following data summary, provide concise, actionable insights:

{data_summary}

Please provide:
1. Key trends and patterns
2. Notable anomalies or outliers
3. Economic implications
4. Forward-looking observations

Keep the response under 300 words and use bullet points."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert economist specializing in global GDP analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return "🤖 **AI-GENERATED INSIGHTS**\n\n" + response.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ Error generating AI insights: {str(e)}\n\nUsing statistical insights instead."


def generate_country_comparison_insights(
    df: pd.DataFrame,
    countries: List[str],
    year_range: tuple = None
) -> str:
    """
    Generate comparative insights for multiple countries.
    
    Args:
        df: DataFrame with GDP data
        countries: List of countries to compare
        year_range: Optional year range for analysis
        
    Returns:
        Formatted comparison insights
    """
    insights = []
    
    insights.append(f"🌍 **COMPARATIVE ANALYSIS**\n")
    
    if year_range:
        df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
        insights.append(f"**Period:** {year_range[0]}-{year_range[1]}\n")
    
    insights.append(f"**Countries Analyzed:** {', '.join(countries)}\n")
    
    # Calculate metrics for each country
    insights.append(f"**Performance Metrics:**")
    
    for country in countries:
        country_data = df[df['country_name'] == country]
        if len(country_data) > 0:
            avg = country_data['gdp_growth'].mean()
            std = country_data['gdp_growth'].std()
            insights.append(f"• {country}: {avg:.2f}% avg (±{std:.2f}% volatility)")
    
    # Identify leader
    country_avgs = {c: df[df['country_name'] == c]['gdp_growth'].mean() 
                   for c in countries if len(df[df['country_name'] == c]) > 0}
    
    if country_avgs:
        leader = max(country_avgs, key=country_avgs.get)
        insights.append(f"\n**Growth Leader:** {leader} ({country_avgs[leader]:.2f}% average)")
    
    return "\n".join(insights)
