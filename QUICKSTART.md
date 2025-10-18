# 🚀 Quick Start Guide

Get the GDP Analytics Dashboard running in 5 minutes!

## ⚡ Fast Track

```bash
# 1. Navigate to project directory
cd gdp-analytics-dashboard

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the dashboard
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

## 📱 First Steps

### 1. Explore the Data
- Go to **"Exploratory Data Analysis"** tab
- Use year range slider to filter data
- Select countries from the dropdown
- View interactive charts

### 2. Make a Forecast
- Go to **"ML Forecasting"** tab
- Select a country (e.g., "United States")
- Choose a model (try **Prophet** for beginners)
- Set forecast horizon to **5 years**
- Click **"Run Forecast"**

### 3. Simulate Policy Impact
- Go to **"Policy Simulation"** tab
- Select a country
- Move the **"Tariff Change"** slider
- Watch the impact calculations update in real-time

### 4. Generate Report
- Go to **"Insights & Reports"** tab
- Click **"Generate PDF Report"**
- Download your analysis

## 🎓 Learning Path

### Beginner (15 minutes)
1. ✅ Explore EDA visualizations
2. ✅ Run a simple forecast
3. ✅ Generate a report

### Intermediate (30 minutes)
1. ✅ Compare multiple countries
2. ✅ Try different forecasting models
3. ✅ Simulate various policy scenarios
4. ✅ Analyze regional correlations

### Advanced (1 hour+)
1. ✅ Upload custom GDP data
2. ✅ Fine-tune model parameters
3. ✅ Create custom insights
4. ✅ Export data for further analysis

## 💡 Tips & Tricks

### Performance
- Use **year range filters** to speed up visualizations
- **Cache** is enabled - first load might be slow
- Refresh page to reset all selections

### Data Upload
Your CSV should have this format:
```csv
country_name,indicator_name,1980,1981,...,2024
United States,GDP growth (%),2.5,3.1,...,2.8
```

### Best Practices
- **ARIMA**: Best for short-term forecasts (1-3 years)
- **Prophet**: Best for long-term forecasts (5-10 years)
- **XGBoost**: Best for complex patterns

### Troubleshooting

**Dashboard won't start?**
```bash
pip install --upgrade streamlit
streamlit run app.py
```

**Import errors?**
```bash
pip install -r requirements.txt --force-reinstall
```

**No visualizations showing?**
- Check browser console (F12)
- Try a different browser
- Clear browser cache

**Model errors?**
- Ensure country has sufficient historical data (10+ years)
- Try a different model
- Adjust year range

## 🎯 Common Use Cases

### Compare USA vs China
1. Go to EDA tab
2. Select both countries in multi-select
3. View time series comparison
4. Note the different growth patterns

### Forecast India's Growth
1. Go to Forecasting tab
2. Select "India"
3. Use Prophet model
4. Set 10-year horizon
5. Analyze the upward trend

### Simulate Trade War
1. Go to Policy Simulation
2. Select a trade-dependent economy (e.g., "Singapore")
3. Set tariff change to +10%
4. Observe the significant negative impact

### Generate Portfolio Report
1. Filter data for recent years (2015-2024)
2. Select your countries of interest
3. Go to Insights & Reports
4. Generate professional PDF
5. Add to your portfolio/presentation

## 📚 Next Steps

- Read full [README.md](README.md) for detailed documentation
- Explore [Jupyter notebook](notebooks/eda.ipynb) for deeper analysis
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to add features
- Deploy to Streamlit Cloud (see README)

## 🆘 Need Help?

- 📖 Read the [full documentation](README.md)
- 🐛 [Report issues](https://github.com/yourusername/gdp-dashboard/issues)
- 💬 Ask questions in discussions
- 📧 Email: your.email@example.com

---

**Happy Analyzing! 📊🌍**
