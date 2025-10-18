"""
Tariff policy simulation module for GDP impact analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class TariffSimulator:
    """
    Simulate the impact of tariff changes on GDP growth.
    
    This uses a simplified economic model where tariff changes affect GDP growth
    through trade elasticity and multiplier effects.
    """
    
    def __init__(self, base_elasticity: float = -0.15):
        """
        Initialize tariff simulator.
        
        Args:
            base_elasticity: Base elasticity factor (how much 1% tariff change affects GDP)
                           Typical range: -0.1 to -0.3 (negative = tariffs hurt growth)
        """
        self.base_elasticity = base_elasticity
        
        # Country-specific adjustments based on trade openness
        self.country_adjustments = {
            'United States': 0.9,      # Less dependent on trade
            'China': 1.2,              # More dependent on trade
            'Germany': 1.3,            # Highly export-oriented
            'Singapore': 1.5,          # Very trade-dependent
            'India': 1.0,              # Moderate
            'Japan': 1.1,              # Export-oriented
            'Brazil': 0.95,            # Less open
            'Mexico': 1.25,            # Highly integrated with US
            'United Kingdom': 1.1,     # Moderate-high
            'Canada': 1.2,             # Trade-dependent
        }
    
    def calculate_impact(
        self, 
        baseline_gdp_growth: float, 
        tariff_change: float, 
        country: str = None
    ) -> Dict:
        """
        Calculate the impact of a tariff change on GDP growth.
        
        Args:
            baseline_gdp_growth: Baseline GDP growth rate (%)
            tariff_change: Change in tariff rate (percentage points)
            country: Country name (for country-specific adjustments)
            
        Returns:
            Dictionary with impact analysis
        """
        # Get country-specific elasticity
        country_factor = self.country_adjustments.get(country, 1.0)
        effective_elasticity = self.base_elasticity * country_factor
        
        # Calculate direct impact
        direct_impact = effective_elasticity * tariff_change
        
        # Add multiplier effect (indirect impacts)
        multiplier = 1.3  # Economic multiplier
        total_impact = direct_impact * multiplier
        
        # Calculate new GDP growth
        new_gdp_growth = baseline_gdp_growth + total_impact
        
        return {
            'baseline_growth': baseline_gdp_growth,
            'tariff_change': tariff_change,
            'direct_impact': direct_impact,
            'multiplier_effect': direct_impact * (multiplier - 1),
            'total_impact': total_impact,
            'new_growth': new_gdp_growth,
            'growth_change_pct': (total_impact / baseline_gdp_growth * 100) if baseline_gdp_growth != 0 else 0
        }
    
    def simulate_scenarios(
        self,
        baseline_gdp_growth: float,
        tariff_scenarios: List[float],
        country: str = None
    ) -> pd.DataFrame:
        """
        Simulate multiple tariff scenarios.
        
        Args:
            baseline_gdp_growth: Baseline GDP growth rate (%)
            tariff_scenarios: List of tariff change values to simulate
            country: Country name
            
        Returns:
            DataFrame with scenario results
        """
        results = []
        
        for tariff in tariff_scenarios:
            impact = self.calculate_impact(baseline_gdp_growth, tariff, country)
            results.append({
                'scenario': f'Tariff {"+" if tariff > 0 else ""}{tariff}%',
                'tariff_change': tariff,
                'baseline_growth': baseline_gdp_growth,
                'projected_growth': impact['new_growth'],
                'total_impact': impact['total_impact'],
                'impact_category': self._categorize_impact(impact['total_impact'])
            })
        
        return pd.DataFrame(results)
    
    def _categorize_impact(self, impact: float) -> str:
        """Categorize the magnitude of impact."""
        if impact < -1.0:
            return 'Severe Negative'
        elif impact < -0.5:
            return 'Moderate Negative'
        elif impact < -0.1:
            return 'Slight Negative'
        elif impact < 0.1:
            return 'Minimal'
        elif impact < 0.5:
            return 'Slight Positive'
        elif impact < 1.0:
            return 'Moderate Positive'
        else:
            return 'Strong Positive'
    
    def forecast_with_policy(
        self,
        baseline_forecast: np.ndarray,
        tariff_change: float,
        country: str = None,
        years: int = 5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply tariff policy to a baseline forecast.
        
        Args:
            baseline_forecast: Array of baseline GDP growth forecasts
            tariff_change: Tariff change to apply
            country: Country name
            years: Number of years to forecast
            
        Returns:
            Tuple of (baseline, policy-adjusted forecast)
        """
        policy_forecast = []
        
        for i, baseline_growth in enumerate(baseline_forecast[:years]):
            # Impact diminishes over time
            time_decay = 0.9 ** i  # 10% decay per year
            adjusted_tariff = tariff_change * time_decay
            
            impact = self.calculate_impact(baseline_growth, adjusted_tariff, country)
            policy_forecast.append(impact['new_growth'])
        
        return baseline_forecast[:years], np.array(policy_forecast)
    
    def generate_policy_report(
        self,
        country: str,
        baseline_growth: float,
        tariff_change: float
    ) -> str:
        """
        Generate a text report on policy impact.
        
        Args:
            country: Country name
            baseline_growth: Baseline GDP growth
            tariff_change: Tariff change amount
            
        Returns:
            Formatted policy report
        """
        impact = self.calculate_impact(baseline_growth, tariff_change, country)
        
        report = f"""
📊 TARIFF POLICY IMPACT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Country: {country}
Tariff Change: {tariff_change:+.1f} percentage points

BASELINE SCENARIO
├─ GDP Growth: {baseline_growth:.2f}%

POLICY-ADJUSTED SCENARIO
├─ Direct Impact: {impact['direct_impact']:.3f}%
├─ Multiplier Effect: {impact['multiplier_effect']:.3f}%
├─ Total Impact: {impact['total_impact']:.3f}%
└─ New GDP Growth: {impact['new_growth']:.2f}%

IMPACT SUMMARY
The proposed tariff change of {tariff_change:+.1f}pp is projected to:
• {"Reduce" if impact['total_impact'] < 0 else "Increase"} GDP growth by {abs(impact['total_impact']):.3f} percentage points
• Result in a {abs(impact['growth_change_pct']):.1f}% {"decrease" if impact['total_impact'] < 0 else "increase"} from baseline
• Impact Category: {self._categorize_impact(impact['total_impact'])}

ECONOMIC CONTEXT
Trade openness factor: {self.country_adjustments.get(country, 1.0):.2f}x
Base elasticity: {self.base_elasticity:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return report


class TradeWarSimulator:
    """
    Simulate complex trade war scenarios with retaliatory measures.
    """
    
    def __init__(self):
        """Initialize trade war simulator."""
        self.tariff_sim = TariffSimulator()
    
    def simulate_trade_war(
        self,
        countries: List[str],
        baseline_growth: Dict[str, float],
        initial_tariff: float,
        retaliation_factor: float = 0.8
    ) -> pd.DataFrame:
        """
        Simulate a trade war with retaliatory tariffs.
        
        Args:
            countries: List of countries involved
            baseline_growth: Dictionary of baseline GDP growth by country
            initial_tariff: Initial tariff imposed
            retaliation_factor: How much retaliation (0.8 = 80% of original)
            
        Returns:
            DataFrame with trade war impact results
        """
        results = []
        
        for country in countries:
            base_growth = baseline_growth.get(country, 2.0)
            
            # Initiating country faces retaliation
            total_tariff_impact = initial_tariff + (initial_tariff * retaliation_factor)
            
            impact = self.tariff_sim.calculate_impact(
                base_growth, 
                total_tariff_impact, 
                country
            )
            
            results.append({
                'country': country,
                'baseline_growth': base_growth,
                'tariff_imposed': initial_tariff,
                'retaliatory_tariff': initial_tariff * retaliation_factor,
                'total_impact': impact['total_impact'],
                'new_growth': impact['new_growth']
            })
        
        return pd.DataFrame(results)
