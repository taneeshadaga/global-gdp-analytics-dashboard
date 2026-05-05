"""
World GDP Growth Analytics Dashboard
Interactive Streamlit application for analyzing global GDP trends with ML forecasting and policy simulation.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add utils and models to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from utils.data_loader import (
    load_and_clean_data, get_country_data, get_regional_data,
    calculate_summary_stats, get_top_performers, get_bottom_performers,
    detect_recessions, calculate_volatility, prepare_ml_data
)
from utils.visualizations import (
    create_time_series_plot, create_regional_comparison, create_top_performers_bar,
    create_correlation_heatmap, create_forecast_plot, create_policy_comparison_plot,
    create_impact_waterfall, create_world_map, create_volatility_plot
)
from utils.ai_insights import (
    generate_statistical_insights, generate_forecast_insights,
    generate_policy_insights, generate_country_comparison_insights
)
from utils.report_generator import generate_pdf_report, generate_html_report, create_summary_report

from models.forecasting import ARIMAForecaster, ProphetForecaster, XGBoostForecaster, compare_models
from models.policy_simulation import TariffSimulator, TradeWarSimulator

# Page configuration
st.set_page_config(
    page_title="Global GDP Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(file_path):
    """Load and cache data."""
    return load_and_clean_data(file_path)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">🌍 World GDP Growth Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**Analyze global GDP trends, forecast future growth, and simulate policy impacts**")
    st.markdown("---")
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Configuration")
    
    # Data loading
    data_file = st.sidebar.file_uploader(
        "Upload GDP Data CSV (optional)",
        type=['csv'],
        help="Upload your own GDP data or use the sample dataset"
    )
    
    if data_file is not None:
        df = load_and_clean_data(data_file)
    else:
        # Use default sample data
        default_path = 'data/world_gdp_data.csv'
        if os.path.exists(default_path):
            df = load_data(default_path)
        else:
            st.error("❌ Sample data file not found. Please upload a CSV file.")
            st.stop()
    
    # Global filters
    st.sidebar.subheader("🎯 Filters")
    
    # Year range selector
    min_year, max_year = int(df['year'].min()), int(df['year'].max())
    year_range = st.sidebar.slider(
        "Year Range",
        min_year, max_year,
        (min_year, max_year)
    )
    
    # Filter data by year range
    df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    # Region filter
    regions = ['All'] + sorted(df['region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Region", regions)
    
    if selected_region != 'All':
        df_filtered = df_filtered[df_filtered['region'] == selected_region]
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Exploratory Data Analysis",
        "🔮 ML Forecasting",
        "🏛️ Policy Simulation",
        "📈 Insights & Reports"
    ])
    
    # ===== TAB 1: EDA =====
    with tab1:
        st.header("Exploratory Data Analysis")
        
        # Summary statistics
        st.subheader("📋 Summary Statistics")
        stats = calculate_summary_stats(df_filtered)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Countries", stats['num_countries'])
        with col2:
            st.metric("Avg GDP Growth", f"{stats['avg_growth']:.2f}%")
        with col3:
            st.metric("Std Deviation", f"{stats['std_growth']:.2f}%")
        with col4:
            st.metric("Total Observations", f"{stats['total_observations']:,}")
        
        st.markdown("---")
        
        # Time series analysis
        st.subheader("📈 Time Series Analysis")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            available_countries = sorted(df_filtered['country_name'].unique())
            selected_countries = st.multiselect(
                "Select Countries",
                available_countries,
                default=available_countries[:5] if len(available_countries) >= 5 else available_countries
            )
        
        with col1:
            if selected_countries:
                fig_ts = create_time_series_plot(
                    df_filtered,
                    selected_countries,
                    f"GDP Growth Trends ({year_range[0]}-{year_range[1]})"
                )
                st.plotly_chart(fig_ts, use_container_width=True)
            else:
                st.info("Select at least one country to view the time series")
        
        st.markdown("---")
        
        # Top and Bottom performers
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top Performers")
            top_n = st.slider("Number of top countries", 5, 20, 10, key='top_n')
            top_performers = get_top_performers(df_filtered, n=top_n)
            
            fig_top = create_top_performers_bar(top_performers, n=top_n)
            st.plotly_chart(fig_top, use_container_width=True)
        
        with col2:
            st.subheader("📉 Bottom Performers")
            bottom_n = st.slider("Number of bottom countries", 5, 20, 10, key='bottom_n')
            bottom_performers = get_bottom_performers(df_filtered, n=bottom_n)
            
            # Reverse for bottom performers
            bottom_performers_sorted = bottom_performers.sort_values('avg_gdp_growth', ascending=True)
            fig_bottom = create_top_performers_bar(bottom_performers_sorted, n=bottom_n)
            st.plotly_chart(fig_bottom, use_container_width=True)
        
        st.markdown("---")
        
        # Regional analysis
        st.subheader("🌏 Regional Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_regional = create_regional_comparison(df_filtered)
            st.plotly_chart(fig_regional, use_container_width=True)
        
        with col2:
            if len(df_filtered['region'].unique()) > 1:
                selected_regions_corr = st.multiselect(
                    "Select regions for correlation analysis",
                    sorted(df_filtered['region'].unique()),
                    default=list(df_filtered['region'].unique())[:5]
                )
                
                if len(selected_regions_corr) >= 2:
                    fig_corr = create_correlation_heatmap(df_filtered, selected_regions_corr)
                    st.plotly_chart(fig_corr, use_container_width=True)
        
        # Volatility analysis
        st.subheader("📊 Volatility Analysis")
        volatility_df = calculate_volatility(df_filtered, window=5)
        
        vol_countries = st.multiselect(
            "Select countries for volatility analysis",
            sorted(df_filtered['country_name'].unique()),
            default=list(df_filtered['country_name'].unique())[:3]
        )
        
        if vol_countries:
            fig_vol = create_volatility_plot(volatility_df, vol_countries)
            st.plotly_chart(fig_vol, use_container_width=True)
    
    # ===== TAB 2: ML FORECASTING =====
    with tab2:
        st.header("Machine Learning Forecasting")
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.subheader("⚙️ Forecast Configuration")
            
            forecast_country = st.selectbox(
                "Select Country",
                sorted(df['country_name'].unique()),
                key='forecast_country'
            )
            
            model_type = st.selectbox(
                "Forecasting Model",
                ['ARIMA', 'Prophet', 'XGBoost'],
                help="Select the machine learning model for forecasting"
            )
            
            forecast_years_num = st.slider(
                "Forecast Horizon (years)",
                1, 10, 5
            )
            
            run_forecast = st.button("🚀 Run Forecast", type="primary")
        
        with col1:
            if run_forecast:
                with st.spinner(f"Training {model_type} model for {forecast_country}..."):
                    # Get country data
                    country_df = get_country_data(df, forecast_country)
                    country_df, X, y = prepare_ml_data(df, forecast_country)
                    
                    # Train model and forecast
                    last_year = country_df['year'].max()
                    forecast_years = np.arange(last_year + 1, last_year + forecast_years_num + 1)
                    
                    try:
                        if model_type == 'ARIMA':
                            model = ARIMAForecaster(order=(2, 1, 2))
                            model.fit(y)
                            forecast, lower, upper = model.predict(steps=forecast_years_num)
                        
                        elif model_type == 'Prophet':
                            model = ProphetForecaster()
                            model.fit(country_df)
                            forecast, lower, upper = model.predict(forecast_years)
                        
                        else:  # XGBoost
                            model = XGBoostForecaster()
                            model.fit(country_df)
                            forecast = model.predict(country_df, forecast_years)
                            # Simple confidence interval for XGBoost
                            std = country_df['gdp_growth'].std()
                            lower = forecast - 1.96 * std
                            upper = forecast + 1.96 * std
                        
                        # Create forecast plot
                        fig_forecast = create_forecast_plot(
                            country_df,
                            forecast_years,
                            forecast,
                            lower,
                            upper,
                            f"{model_type} Forecast for {forecast_country}"
                        )
                        st.plotly_chart(fig_forecast, use_container_width=True)
                        
                        # Display forecast table
                        forecast_df = pd.DataFrame({
                            'Year': forecast_years,
                            'Forecasted GDP Growth (%)': [f"{f:.2f}" for f in forecast],
                            'Lower Bound (%)': [f"{l:.2f}" for l in lower],
                            'Upper Bound (%)': [f"{u:.2f}" for u in upper]
                        })
                        
                        st.subheader("📊 Forecast Results")
                        st.dataframe(forecast_df, use_container_width=True)
                        
                        # Generate insights
                        historical_avg = country_df['gdp_growth'].mean()
                        forecast_avg = forecast.mean()
                        
                        insights = generate_forecast_insights(
                            forecast_country,
                            historical_avg,
                            forecast_avg,
                            model_type
                        )
                        
                        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                        st.markdown(insights)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Store in session state for report generation
                        st.session_state['forecast_results'] = {
                            'country': forecast_country,
                            'model': model_type,
                            'forecast_df': forecast_df,
                            'insights': insights
                        }
                        
                        st.success(f"✅ Forecast completed successfully using {model_type}!")
                    
                    except Exception as e:
                        st.error(f"❌ Error during forecasting: {str(e)}")
                        st.info("Try adjusting the year range or selecting a different model.")
        
        # Model comparison
        st.markdown("---")
        st.subheader("📊 Model Performance Comparison")
        
        if st.button("Compare All Models"):
            with st.spinner("Comparing model performance..."):
                country_df = get_country_data(df, forecast_country)
                
                try:
                    comparison_results = compare_models(country_df, test_size=0.2)
                    
                    # Display comparison
                    comparison_df = pd.DataFrame(comparison_results).T
                    st.dataframe(comparison_df, use_container_width=True)
                    
                    st.info("📌 Lower MAE and RMSE indicate better performance. Higher R² indicates better fit.")
                
                except Exception as e:
                    st.error(f"Error in model comparison: {str(e)}")
    
    # ===== TAB 3: POLICY SIMULATION =====
    with tab3:
        st.header("Tariff Policy Impact Simulation")
        
        st.markdown("""
        Simulate how tariff changes might affect GDP growth. This uses a simplified economic model 
        where tariff changes impact growth through trade elasticity and multiplier effects.
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.subheader("⚙️ Simulation Settings")
            
            policy_country = st.selectbox(
                "Select Country",
                sorted(df['country_name'].unique()),
                key='policy_country'
            )
            
            # Get recent GDP growth
            recent_data = df[df['country_name'] == policy_country].tail(5)
            baseline_growth = recent_data['gdp_growth'].mean()
            
            st.metric("Current Avg GDP Growth", f"{baseline_growth:.2f}%")
            
            tariff_change = st.slider(
                "Tariff Change (percentage points)",
                -10.0, 10.0, 0.0, 0.5,
                help="Positive = tariff increase, Negative = tariff reduction"
            )
            
            elasticity = st.slider(
                "Trade Elasticity",
                -0.5, -0.05, -0.15, 0.01,
                help="How sensitive GDP is to tariff changes (more negative = more sensitive)"
            )
            
            run_simulation = st.button("🎯 Run Simulation", type="primary")
        
        with col1:
            if run_simulation or tariff_change != 0:
                simulator = TariffSimulator(base_elasticity=elasticity)
                
                # Single scenario impact
                impact = simulator.calculate_impact(
                    baseline_growth,
                    tariff_change,
                    policy_country
                )
                
                # Display impact breakdown
                st.subheader("💥 Impact Analysis")
                
                cols = st.columns(4)
                with cols[0]:
                    st.metric(
                        "Baseline Growth",
                        f"{impact['baseline_growth']:.2f}%"
                    )
                with cols[1]:
                    st.metric(
                        "Direct Impact",
                        f"{impact['direct_impact']:.3f}pp",
                        delta=f"{impact['direct_impact']:.3f}pp"
                    )
                with cols[2]:
                    st.metric(
                        "Total Impact",
                        f"{impact['total_impact']:.3f}pp",
                        delta=f"{impact['total_impact']:.3f}pp"
                    )
                with cols[3]:
                    st.metric(
                        "New Growth",
                        f"{impact['new_growth']:.2f}%",
                        delta=f"{impact['new_growth'] - impact['baseline_growth']:.2f}pp"
                    )
                
                # Waterfall chart
                fig_waterfall = create_impact_waterfall(impact)
                st.plotly_chart(fig_waterfall, use_container_width=True)
                
                # Multiple scenarios
                st.subheader("📊 Scenario Comparison")
                
                scenarios = [-5, -2.5, 0, 2.5, 5, 7.5, 10]
                scenarios_df = simulator.simulate_scenarios(
                    baseline_growth,
                    scenarios,
                    policy_country
                )
                
                fig_scenarios = create_policy_comparison_plot(scenarios_df)
                st.plotly_chart(fig_scenarios, use_container_width=True)
                
                st.dataframe(scenarios_df, use_container_width=True)
                
                # Generate policy insights
                policy_insights = generate_policy_insights(
                    policy_country,
                    impact,
                    tariff_change
                )
                
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown(policy_insights)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Store for report
                st.session_state['policy_results'] = {
                    'country': policy_country,
                    'impact': impact,
                    'scenarios_df': scenarios_df,
                    'insights': policy_insights
                }
    
    # ===== TAB 4: INSIGHTS & REPORTS =====
    with tab4:
        st.header("Insights & Reports")
        
        # Statistical insights
        st.subheader("📊 Automated Insights")
        
        stats = calculate_summary_stats(df_filtered)
        insights = generate_statistical_insights(df_filtered, stats)
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown(insights)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Country comparison
        st.subheader("🌍 Country Comparison")
        
        compare_countries = st.multiselect(
            "Select countries to compare",
            sorted(df['country_name'].unique()),
            default=list(df['country_name'].unique())[:3]
        )
        
        if compare_countries and len(compare_countries) >= 2:
            comparison_insights = generate_country_comparison_insights(
                df_filtered,
                compare_countries,
                year_range
            )
            
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown(comparison_insights)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Report generation
        st.markdown("---")
        st.subheader("📥 Download Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Generate PDF Report"):
                with st.spinner("Generating PDF report..."):
                    try:
                        top_perf = get_top_performers(df_filtered, n=10)
                        bottom_perf = get_bottom_performers(df_filtered, n=10)
                        
                        sections = create_summary_report(
                            stats,
                            top_perf,
                            bottom_perf,
                            insights
                        )
                        
                        pdf_bytes = generate_pdf_report(
                            "World GDP Growth Analysis Report",
                            sections
                        )
                        
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_bytes,
                            file_name=f"gdp_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf"
                        )
                        
                        st.success("✅ PDF report generated successfully!")
                    
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
        
        with col2:
            if st.button("🌐 Generate HTML Report"):
                with st.spinner("Generating HTML report..."):
                    try:
                        top_perf = get_top_performers(df_filtered, n=10)
                        bottom_perf = get_bottom_performers(df_filtered, n=10)
                        
                        sections = create_summary_report(
                            stats,
                            top_perf,
                            bottom_perf,
                            insights
                        )
                        
                        html_content = generate_html_report(
                            "World GDP Growth Analysis Report",
                            sections
                        )
                        
                        st.download_button(
                            label="⬇️ Download HTML",
                            data=html_content,
                            file_name=f"gdp_report_{datetime.now().strftime('%Y%m%d')}.html",
                            mime="text/html"
                        )
                        
                        st.success("✅ HTML report generated successfully!")
                    
                    except Exception as e:
                        st.error(f"Error generating HTML: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>World GDP Growth Analytics Dashboard | Built with Streamlit, Plotly, and Machine Learning</p>
            <p>Data source: World GDP Growth (1980-2024) Dataset</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
