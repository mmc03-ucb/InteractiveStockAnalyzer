# Interactive Stock Analyzer

## Overview
Interactive Stock Analyzer is a Python-based application designed for real-time stock data analysis. It utilizes technical indicators such as the Relative Strength Index (RSI) and Bollinger Bands to provide insights into stock market trends. Built using yfinance, Plotly, and Dash, this tool offers an interactive web interface for visualizing stock price movements and indicator signals.

## Features
- **Stock Data Fetching**: Retrieves historical stock data from Yahoo Finance.
- **Technical Indicator Analysis**: Computes RSI and Bollinger Bands to identify potential buy and sell signals.
- **Interactive Dashboards**: Visualizes stock data and indicators using Plotly graphs within a Dash web application.

## Installation

To set up the InteractiveStockAnalyzer, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/mmc03-ucb/InteractiveStockAnalyzer.git
   ```

2. Navigate to the project directory:
   ```
   cd InteractiveStockAnalyzer
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, use the following command:

```
python trading_strategy.py
```

Make sure to modify the `config.json` file with your desired stock symbol and date range for analysis.

## Testing

Run unit tests with:

```
python test_stock_analyzer.py
```

## Configuration

The `config.json` file is used to set the stock symbol and the date range for the analysis. Edit this file to analyze different stocks or time periods.

Example:
```json
{
  "symbol": "NVDA",
  "start_date": "2020-01-01",
  "end_date": "2023-01-01"
}
```

## Contributing

Contributions to the InteractiveStockAnalyzer are welcome. Please ensure to follow the project's code style and add unit tests for any new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
