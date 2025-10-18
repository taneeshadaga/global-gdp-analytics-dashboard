# Contributing to GDP Analytics Dashboard

Thank you for considering contributing to the GDP Analytics Dashboard! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/gdp-dashboard/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs. actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Enhancements

1. Check existing issues and pull requests
2. Create a new issue describing:
   - The enhancement goal
   - Why it would be useful
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation as needed

4. **Test your changes**
   ```bash
   streamlit run app.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/YourFeature
   ```

7. **Submit a Pull Request**
   - Describe what you changed and why
   - Reference any related issues

## 📋 Code Style Guidelines

### Python Code
- Follow **PEP 8** style guide
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for functions and classes

Example:
```python
def calculate_gdp_impact(
    baseline: float,
    tariff_change: float,
    country: str
) -> Dict[str, float]:
    """
    Calculate GDP impact of tariff changes.
    
    Args:
        baseline: Baseline GDP growth rate
        tariff_change: Tariff adjustment in percentage points
        country: Country name
        
    Returns:
        Dictionary containing impact metrics
    """
    # Implementation
```

### Streamlit Code
- Use clear section headers
- Add helpful tooltips (`help="..."` parameter)
- Provide user feedback with `st.success()`, `st.error()`, etc.
- Use `st.cache_data` for expensive operations

### Documentation
- Update README.md for new features
- Add docstrings to new functions
- Comment complex algorithms
- Update requirements.txt if adding dependencies

## 🧪 Testing

Before submitting:

1. **Test the dashboard locally**
   ```bash
   streamlit run app.py
   ```

2. **Check all tabs work correctly**
   - EDA visualizations
   - Forecasting models
   - Policy simulations
   - Report generation

3. **Test with different data**
   - Upload custom CSV files
   - Try different year ranges
   - Test edge cases

4. **Verify no errors in console**

## 🎯 Priority Areas for Contribution

We especially welcome contributions in:

1. **New Forecasting Models**
   - LSTM/RNN implementations
   - Ensemble methods
   - Advanced statistical models

2. **Enhanced Visualizations**
   - More interactive charts
   - 3D visualizations
   - Animation features

3. **Additional Analysis Features**
   - Sector-specific analysis
   - Trade flow analysis
   - Economic indicator correlations

4. **Performance Improvements**
   - Optimization of data loading
   - Caching strategies
   - Async operations

5. **Documentation**
   - Tutorial videos
   - Use case examples
   - API documentation

## 📦 Adding Dependencies

If your contribution requires new packages:

1. Add to `requirements.txt` with version pinning:
   ```
   new-package==1.2.3
   ```

2. Document why it's needed in your PR
3. Ensure it's compatible with Python 3.10+

## 🔍 Code Review Process

1. Maintainers will review your PR within 1 week
2. Feedback will be provided via PR comments
3. Address requested changes
4. Once approved, your PR will be merged

## 💡 Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/gdp-dashboard.git
cd gdp-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙋 Questions?

- Open an issue with the `question` label
- Reach out via email (your.email@example.com)
- Join our discussions

## 🌟 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for helping improve the GDP Analytics Dashboard! 🎉
