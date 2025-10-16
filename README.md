# Generate Charts with Natural Language (Use Your Own CSV or Excel Data)

[English](README.md) | [繁體中文](README.zh-TW.md)

An AI-based data visualization tool that automatically analyzes Excel/CSV files and generates various charts based on natural language descriptions.

## Features

- **LLM-Driven**: Uses Google Gemini API to understand natural language instructions
- **Multi-Format Support**: Supports Excel (.xlsx) and CSV (.csv) files
- **Data Analysis**: Automatically identifies data types (numeric, date, categorical)
- **Chart Support**: Supports bar charts, line charts, scatter plots, pie charts, and more
- **Interactive Visualization**: Interactive charts based on Plotly
- **Safe Execution**: Code safety checks and sandboxed execution environment
- **Retry Mechanism**: Automatic error handling and fallback chart mechanism
- **Responsive Interface**: Modern web interface based on Streamlit

## Quick Start

### Requirements

- Python 3.11 or 3.12 (recommended, Python 3.13 may have compatibility issues)
- Google Gemini API Key

### Installation

#### Method 1: Quick Install (Recommended)

1. **Clone the project**
   ```bash
   git clone https://github.com/chengyimio/CSV_to_Chart_LLM.git
   cd CSV_to_Chart_LLM/excel-chart-generator
   ```

2. **Use the automatic installation script**

   **Windows:**
   ```bash
   python setup.py
   ```

   **macOS/Linux:**
   ```bash
   python3 setup.py
   ```

   The script will automatically:
   - Check Python version
   - Create virtual environment
   - Install all dependencies
   - Create `.env` configuration file

3. **Set up API Key**
   - Go to [Google AI Studio](https://ai.google.dev) to get your Gemini API Key
   - Edit the `excel-chart-generator/.env` file and enter your API Key:
     ```env
     GEMINI_API_KEY=your_api_key_here
     ```

4. **Run the application**

   **Windows:**
   ```bash
   venv\Scripts\activate
   streamlit run app.py
   ```

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

#### Method 2: Manual Installation

1. **Clone the project**
   ```bash
   git clone https://github.com/chengyimio/CSV_to_Chart_LLM.git
   cd CSV_to_Chart_LLM/excel-chart-generator
   ```

2. **Create virtual environment**

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy environment variable template
   cp .env.example .env

   # Edit .env and enter your Gemini API Key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## System Architecture

```
excel-chart-generator/
├── app.py                     # Main application
├── .env                       # Environment configuration
├── requirements.txt           # Project dependencies
├── modules/
│   ├── __init__.py
│   ├── data_analyzer.py       # Data analysis module
│   ├── gemini_client.py       # Gemini API client
│   ├── chart_generator.py     # Chart generator
│   └── module_manager.py      # Module management configuration
└── uploads/                   # Temporary upload files
```

## Usage

### Basic Workflow

1. **Upload Data File**: Supports Excel (.xlsx) or CSV (.csv)
2. **Analyze Data Structure**: System automatically identifies field types
3. **Describe Chart Requirements**: Describe the desired chart in natural language
4. **Generate Visualization**: AI automatically generates and displays the chart

### Example Commands

```
Basic Charts:
- "Draw a bar chart of sales"
- "Show the trend chart by month"
- "Create a pie chart of product categories"

Advanced Charts:
- "Compare sales performance across regions using a grouped bar chart"
- "Analyze the correlation between price and quantity using a scatter plot"
- "Show trend changes in time series data"

Statistical Analysis:
- "Show the distribution of the data"
- "Compare average values across different categories"
- "Analyze correlations between variables"
```

## Tech Stack

### Core Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data processing and analysis
- **Plotly**: Interactive charting library
- **Matplotlib & Seaborn**: Statistical charts
- **Google GenerativeAI**: Gemini API client
- **NumPy**: Numerical computing support

### Optional Dependencies (Advanced Features)
- **Statsmodels**: Statistical analysis
- **Scikit-learn**: Machine learning
- **SciPy**: Scientific computing

## Configuration

### requirements.txt
```txt
# Core dependencies
streamlit==1.40.0
pandas==2.2.3
numpy==1.24.4
openpyxl==3.1.5
plotly==5.24.1
matplotlib==3.9.2
seaborn==0.13.2
google-generativeai==0.8.3
python-dotenv==1.0.1

# Optional dependencies
statsmodels==0.14.0
scipy==1.11.4
scikit-learn==1.3.2
```

### .env File Example
```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_api_key_here

# Optional Configuration
MAX_FILE_SIZE_MB=50
DEFAULT_CHART_TYPE=plotly
DEBUG_MODE=false
```

## Supported Chart Types

| Chart Type | Use Case | Example Command |
|-----------|----------|-----------------|
| Bar Chart | Category comparison | "Compare sales by product" |
| Line Chart | Trend analysis | "Monthly sales trend" |
| Scatter Plot | Correlation analysis | "Relationship between price and sales" |
| Pie Chart | Proportion display | "Market share distribution" |
| Histogram | Distribution analysis | "Age distribution" |
| Box Plot | Statistical summary | "Distribution characteristics of each group" |
| Heatmap | Correlation matrix | "Correlation analysis between variables" |

## Troubleshooting

### Common Issues

**1. Installation Failure (Python 3.13 compatibility issues)**
```bash
# Solution: Use Python 3.11 or 3.12
python --version  # Check version
pip install --upgrade pip setuptools
```

**2. API Key Error**
```bash
# Check if .env file is configured correctly
# Verify API Key validity
```

**3. Module Import Error**
```bash
# Reinstall dependencies
pip install --upgrade --force-reinstall -r requirements.txt
```

**4. Chart Generation Failure**
- Check if data format is correct
- Confirm field names match
- Try simpler chart descriptions

### Performance Optimization

- **Large Files**: Recommended to keep data volume under 5000 rows
- **Memory Usage**: Can adjust Streamlit's memory configuration
- **API Quota**: Be mindful of Gemini API usage limits

## Contributing

Contributions, bug reports, and improvement suggestions are welcome!

### Development Environment Setup
1. Fork the project
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Create a Pull Request

### Code Standards
- Follow Python PEP 8 style
- Add appropriate comments and documentation
- Ensure backward compatibility
- Include test cases

## Support and Feedback

If you encounter problems or have suggestions for improvement:

- **Report Bugs**: Please describe the issue in detail in Issues
- **Feature Suggestions**: Welcome to propose new feature ideas
- **Contact Us**: [chengyimio@gmail.com]
- **Documentation Issues**: Help improve the documentation

---

## Future Plans

- [ ] Support more file formats (JSON, XML)
- [ ] Add dashboard functionality
- [ ] Multi-language support
- [ ] Chart export functionality (PNG, PDF)
- [ ] Data cleaning suggestions
- [ ] Collaboration features
- [ ] Custom chart styles
- [ ] API interface development

## Version History

### v1.0.0 (Current Version)
- Basic chart generation functionality
- Excel/CSV file support
- Gemini AI integration
- Secure code execution
- Responsive UI

---

**If this project helps you, please give us a Star!**
