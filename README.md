# 🌍 World GDP Growth Analytics Dashboard

<div align="center">

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Interactive web dashboard for analyzing global GDP trends with ML forecasting and policy simulation**

[Features](#-core-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Demo](#-demo)

</div>

---

## 📖 Overview

This Streamlit-based dashboard provides comprehensive analysis of **World GDP Growth (1980–2024)** with advanced features including:
- 📊 Interactive exploratory data analysis (EDA)
- 🔮 Machine learning forecasting (ARIMA, Prophet, XGBoost)
- 🏛️ Tariff policy impact simulation
- 📈 Automated insights generation
- 📥 Downloadable PDF/HTML reports

Perfect for **data scientists**, **economists**, **policy analysts**, and anyone interested in global economic trends.

---

## ✨ Core Features

### 1️⃣ Exploratory Data Analysis (EDA)
- **Summary Statistics**: Key metrics for 40+ countries across 45 years
- **Interactive Charts**: Time series, regional comparisons, correlation heatmaps
- **Top/Bottom Performers**: Identify fastest and slowest growing economies
- **Volatility Analysis**: Track economic stability over time
- **Crisis Detection**: Analyze impact of 2008 Financial Crisis, COVID-19, etc.

### 2️⃣ Machine Learning Forecasting
- **Multiple Models**: ARIMA, Prophet, XGBoost
- **Forecast Horizon**: 1-10 year predictions with confidence intervals
- **Model Comparison**: Evaluate performance using MAE, RMSE, R²
- **Interactive Visualization**: Historical data vs. forecasts

### 3️⃣ Tariff Policy Simulation
- **Impact Analysis**: Estimate how tariff changes affect GDP growth
- **Economic Modeling**: Trade elasticity and multiplier effects
- **Scenario Comparison**: Test multiple policy scenarios simultaneously
- **Waterfall Charts**: Visualize impact breakdown
- **Country-Specific Adjustments**: Based on trade openness

### 4️⃣ Insights & Reporting
- **Automated Insights**: Statistical analysis and trend identification
- **Country Comparisons**: Multi-country analysis with visualizations
- **PDF Reports**: Professional downloadable reports
- **HTML Reports**: Interactive web-based reports
- **AI Insights** (Optional): GPT-powered economic analysis with API key

---

## 🚀 Installation

### Prerequisites
- Python 3.13+ (or 3.10+)
- pip package manager
- (Optional) Virtual environment

### Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd gdp-analytics-dashboard
```

2. **Create virtual environment** (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the dashboard**
```bash
streamlit run app.py
```

5. **Open in browser**
The dashboard will automatically open at `http://localhost:8501`

---

## 📊 Usage

### Starting the Dashboard

```bash
streamlit run app.py
```

### Uploading Custom Data

1. Click **"Upload GDP Data CSV"** in the sidebar
2. Upload a CSV file with format:
   ```
   country_name,indicator_name,1980,1981,...,2024
   United States,GDP growth (%),2.5,3.1,...,2.8
   ```
3. The dashboard will automatically process and visualize your data

### Using the Features

#### **EDA Tab**
1. Select year range and region filters
2. Choose countries for time series analysis
3. Explore top/bottom performers, regional comparisons
4. Analyze volatility trends

#### **Forecasting Tab**
1. Select a country
2. Choose forecasting model (ARIMA/Prophet/XGBoost)
3. Set forecast horizon (1-10 years)
4. Click **"Run Forecast"**
5. View predictions with confidence intervals
6. Compare model performance

#### **Policy Simulation Tab**
1. Select a country
2. Adjust tariff change slider (-10% to +10%)
3. Modify trade elasticity if needed
4. Click **"Run Simulation"**
5. View impact analysis and scenario comparisons

#### **Insights & Reports Tab**
1. Review automated statistical insights
2. Compare multiple countries
3. Generate and download PDF/HTML reports

---

## 📁 Project Structure

```
gdp-analytics-dashboard/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── data/
│   ├── world_gdp_data.csv         # Sample GDP dataset
│   └── sample_data_generator.py   # Script to generate sample data
│
├── models/
│   ├── forecasting.py             # ML forecasting models (ARIMA, Prophet, XGBoost)
│   └── policy_simulation.py       # Tariff impact simulation engine
│
├── utils/
│   ├── data_loader.py             # Data loading and preprocessing
│   ├── visualizations.py          # Plotly chart generators
│   ├── ai_insights.py             # Insights generation (with optional GPT)
│   └── report_generator.py        # PDF/HTML report creation
│
├── notebooks/
│   └── eda.ipynb                  # Exploratory data analysis notebook
│
└── .streamlit/
    └── config.toml                # Streamlit configuration
```

---

## 🛠️ Tech Stack

### Core Framework
- **Streamlit** (1.31.0) - Interactive web framework
- **Python** (3.13+) - Programming language

### Data Processing
- **pandas** (2.2.0) - Data manipulation
- **NumPy** (1.26.3) - Numerical computing

### Visualization
- **Plotly** (5.18.0) - Interactive charts
- **Matplotlib** (3.8.2) - Static visualizations
- **Seaborn** (0.13.1) - Statistical plots

### Machine Learning
- **scikit-learn** (1.4.0) - ML utilities
- **Prophet** (1.1.5) - Facebook's forecasting library
- **statsmodels** (0.14.1) - ARIMA models
- **XGBoost** (2.0.3) - Gradient boosting

### Reporting
- **ReportLab** (4.0.9) - PDF generation
- **Pillow** (10.2.0) - Image processing

### Optional
- **OpenAI** (1.12.0) - AI-powered insights (requires API key)

---

## 📚 Documentation

### Data Format

The dashboard expects GDP data in **wide format**:

| country_name | indicator_name | 1980 | 1981 | ... | 2024 |
|--------------|----------------|------|------|-----|------|
| United States | GDP growth (annual %) | 2.5 | 3.1 | ... | 2.8 |
| China | GDP growth (annual %) | 7.8 | 5.2 | ... | 4.6 |

The system automatically converts this to **long format** for analysis:

| country_name | year | gdp_growth | region |
|--------------|------|------------|--------|
| United States | 1980 | 2.5 | North America |
| United States | 1981 | 3.1 | North America |

### Forecasting Models

#### **ARIMA (AutoRegressive Integrated Moving Average)**
- Best for: Time series with trends and seasonality
- Parameters: (p=2, d=1, q=2) - auto-configured
- Output: Point forecast + 95% confidence intervals

#### **Prophet**
- Best for: Long-term forecasts with multiple seasonality
- Features: Handles missing data, outliers, holidays
- Output: Forecast with uncertainty bounds

#### **XGBoost**
- Best for: Complex non-linear patterns
- Features: Lag features, rolling statistics, year trends
- Output: Point forecast with empirical confidence intervals

### Policy Simulation Model

The tariff simulation uses a simplified economic model:

```
GDP Impact = (Tariff Change × Elasticity × Country Factor) × Multiplier
```

Where:
- **Elasticity**: Base impact factor (default: -0.15)
- **Country Factor**: Trade openness adjustment (0.9-1.5x)
- **Multiplier**: Economic multiplier effect (default: 1.3x)

---

## 🎯 Use Cases

### For Data Scientists
- Explore GDP trends and patterns
- Build and compare forecasting models
- Analyze regional correlations
- Generate data-driven insights

### For Economists
- Track global economic performance
- Study crisis impacts (2008, COVID-19)
- Compare country/regional trajectories
- Identify growth opportunities

### For Policy Analysts
- Simulate tariff policy impacts
- Evaluate trade policy scenarios
- Assess economic risks
- Support evidence-based decisions

### For Students & Researchers
- Learn time series forecasting
- Study economic indicators
- Practice data visualization
- Build portfolio projects

---

## 🌟 Advanced Features

### AI Economist Mode (Optional)

Enable GPT-powered insights by setting your OpenAI API key:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

The AI will:
- Generate natural language insights
- Interpret complex patterns
- Provide policy recommendations
- Create executive summaries

### Custom Regional Mapping

Edit `utils/data_loader.py` to add/modify country-region mappings:

```python
COUNTRY_REGION_MAPPING = {
    'Your Country': 'Your Region',
    ...
}
```

### Model Fine-Tuning

Adjust forecasting parameters in `models/forecasting.py`:

```python
# ARIMA
ARIMAForecaster(order=(p, d, q))

# XGBoost
XGBoostForecaster(n_estimators=100, learning_rate=0.1)
```

---

## 📊 Demo

### Screenshots

**EDA Dashboard**
- Interactive time series plots
- Regional comparisons
- Top/bottom performers

**ML Forecasting**
- Multiple model support
- Confidence intervals
- Model comparison metrics

**Policy Simulation**
- Impact waterfall charts
- Scenario comparisons
- Automated insights

---

## 🚢 Deployment

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect GitHub repository
4. Deploy with one click

### Hugging Face Spaces

1. Create new Space at [huggingface.co](https://huggingface.co)
2. Select Streamlit SDK
3. Upload project files
4. App will auto-deploy

### Docker

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t gdp-dashboard .
docker run -p 8501:8501 gdp-dashboard
```

---

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 Data Source

Sample data generated for demonstration purposes, modeled after:
- **Kaggle**: World GDP Growth (1980-2024) by Sazidul Islam
- **World Bank**: GDP growth (annual %) indicators
- **IMF**: World Economic Outlook Database

For production use, download official data from:
- [World Bank Open Data](https://data.worldbank.org)
- [IMF Data](https://www.imf.org/en/Data)
- [OECD Data](https://data.oecd.org)

---

## ⚠️ Disclaimer

This dashboard is for **educational and analytical purposes only**. The forecasts and policy simulations are based on simplified models and should not be used as the sole basis for financial or policy decisions. Always consult professional economists and use official data sources for critical analysis.

---

## 📄 License

This project is licensed under the **MIT License** - see LICENSE file for details.

---

## 👤 Author

**Your Name**
- Portfolio: [your-portfolio.com](https://your-portfolio.com)
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- GitHub: [@yourusername](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- **Streamlit Team** - Amazing framework
- **Prophet Team** - Robust forecasting library
- **Plotly Team** - Beautiful visualizations
- **Data Providers** - World Bank, IMF, OECD

---

## 📧 Contact

Questions? Suggestions? Reach out:
- Email: your.email@example.com
- Issues: [GitHub Issues](https://github.com/yourusername/gdp-dashboard/issues)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ and Python

</div>
