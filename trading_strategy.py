import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from dash import Dash, html, dcc, dependencies
import logging
import argparse
import json
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands


# Class Definition
class StockAnalyzer:
    def __init__(self, symbol, start, end):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = None

    def fetch_data(self):
        """Fetch stock data from Yahoo Finance."""
        try:
            self.data = yf.download(self.symbol, start=self.start, end=self.end)
            logging.info(f"Data fetched successfully for {self.symbol}.")
        except Exception as e:
            logging.error(f"Error fetching data for {self.symbol}: {e}")
            self.data = None

    def calculate_technical_indicators(self):
        """Calculate technical indicators such as RSI and Bollinger Bands."""
        if self.data is not None:
            rsi = RSIIndicator(self.data["Adj Close"]).rsi()
            bollinger = BollingerBands(self.data["Adj Close"])
            self.data["RSI"] = rsi
            self.data["Bollinger_High"] = bollinger.bollinger_hband()
            self.data["Bollinger_Low"] = bollinger.bollinger_lband()

    def create_dash_app(self):
        """Create a Dash app for interactive visualization."""
        app = Dash(__name__)
        app.layout = html.Div(
            [
                html.H1(f"{self.symbol} Stock Data"),
                html.Div(
                    [
                        html.H2("Relative Strength Index (RSI)"),
                        html.P(
                            "The RSI is a momentum indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock."
                        ),
                        html.P(
                            "Generally, an RSI above 70 indicates a potential sell signal as the stock might be overbought, while an RSI below 30 suggests a potential buy signal as the stock might be oversold."
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H2("Bollinger Bands"),
                        html.P(
                            "Bollinger Bands consist of a middle band being an N-period simple moving average (SMA), an upper band at K times an N-period standard deviation above the SMA, and a lower band at K times an N-period standard deviation below the SMA."
                        ),
                        html.P(
                            "Traders might consider selling when the price touches the upper band and buying when it hits the lower band."
                        ),
                    ]
                ),
                dcc.Graph(id="stock-graph"),
                dcc.Interval(
                    id="interval-component",
                    interval=1 * 60000,  # in milliseconds
                    n_intervals=0,
                ),
            ]
        )

        @app.callback(
            dependencies.Output("stock-graph", "figure"),
            [dependencies.Input("interval-component", "n_intervals")],
        )
        def update_graph_live(n):
            self.fetch_data()
            self.calculate_technical_indicators()

            # Create Plotly figure
            fig = go.Figure()

            # Plot Adjusted Close Price
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.data["Adj Close"],
                    mode="lines",
                    name="Adjusted Close",
                )
            )

            # Plot RSI
            fig.add_trace(
                go.Scatter(
                    x=self.data.index, y=self.data["RSI"], mode="lines", name="RSI"
                )
            )

            # Plot Bollinger Bands
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.data["Bollinger_High"],
                    mode="lines",
                    name="Bollinger High",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=self.data.index,
                    y=self.data["Bollinger_Low"],
                    mode="lines",
                    name="Bollinger Low",
                )
            )

            # Mark Buy and Sell Signals
            buy_signals = self.data[
                (self.data["RSI"] < 30)
                | (self.data["Adj Close"] < self.data["Bollinger_Low"])
            ]
            sell_signals = self.data[
                (self.data["RSI"] > 70)
                | (self.data["Adj Close"] > self.data["Bollinger_High"])
            ]

            fig.add_trace(
                go.Scatter(
                    x=buy_signals.index,
                    y=buy_signals["Adj Close"],
                    mode="markers",
                    marker=dict(color="green", size=10),
                    name="Buy Signal",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=sell_signals.index,
                    y=sell_signals["Adj Close"],
                    mode="markers",
                    marker=dict(color="red", size=10),
                    name="Sell Signal",
                )
            )

            return fig

        return app


# Main function
def main():
    parser = argparse.ArgumentParser(
        description="Stock Data Analysis with Technical Indicators"
    )
    parser.add_argument("config", type=str, help="Configuration file (JSON format)")
    args = parser.parse_args()

    with open(args.config, "r") as config_file:
        config = json.load(config_file)

    stock_analyzer = StockAnalyzer(
        config["symbol"], config["start_date"], config["end_date"]
    )
    app = stock_analyzer.create_dash_app()
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
