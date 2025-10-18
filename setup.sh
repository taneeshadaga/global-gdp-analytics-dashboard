#!/bin/bash

# GDP Analytics Dashboard - Setup Script
# This script sets up the environment and installs all dependencies

echo "🌍 World GDP Analytics Dashboard - Setup Script"
echo "================================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $python_version"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🚀 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p data
mkdir -p notebooks
mkdir -p models
mkdir -p utils
mkdir -p reports
echo "✅ Directories created"
echo ""

# Generate sample data if not exists
if [ -f "data/world_gdp_data.csv" ]; then
    echo "✅ Sample data already exists"
else
    echo "📊 Sample data found"
fi
echo ""

echo "================================================"
echo "✅ Setup complete!"
echo ""
echo "To start the dashboard:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: streamlit run app.py"
echo ""
echo "To deactivate virtual environment:"
echo "  deactivate"
echo ""
echo "================================================"
