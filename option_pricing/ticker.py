import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent / "data_cache"

class Ticker:
    @staticmethod
    def _normalize_ticker(ticker):
        return ticker.strip().upper()

    @staticmethod
    def _cache_path(ticker):
        return CACHE_DIR / f"{Ticker._normalize_ticker(ticker)}_history.csv"

    @staticmethod
    def _read_cached_historical_data(ticker):
        cache_path = Ticker._cache_path(ticker)
        if not cache_path.exists():
            return None

        data = pd.read_csv(cache_path, index_col="Date", parse_dates=True)
        if data.empty:
            return None
        data.index.name = "Date"
        return data

    @staticmethod
    def _write_cached_historical_data(ticker, data):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        data.to_csv(Ticker._cache_path(ticker), index_label="Date")

    @staticmethod
    def get_historical_data(ticker, start_date=None, end_date=None):
        ticker = Ticker._normalize_ticker(ticker)
        use_cache = start_date is None and end_date is None

        if use_cache:
            cached_data = Ticker._read_cached_historical_data(ticker)
            if cached_data is not None:
                return cached_data
        try:
            if start_date is None:
                start_date = datetime.datetime.now() - datetime.timedelta(days=365)
            if end_date is None:
                end_date = datetime.datetime.now()
            
            stock = yf.Ticker(ticker)
            data = stock.history(start=start_date, end=end_date)
            
            if data.empty:
                raise ValueError(f"No data returned for ticker {ticker}")
            if use_cache:
                Ticker._write_cached_historical_data(ticker, data)
            return data
        except Exception as e:
            raise Exception(f"Error fetching data for ticker {ticker}: {str(e)}")

    @staticmethod
    def get_columns(data):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        return list(data.columns)

    @staticmethod
    def get_last_price(data, column_name):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        if column_name not in data.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame")
        return data[column_name].iloc[-1]

    @staticmethod
    def plot_data(data, ticker, column_name):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        if column_name not in data.columns:
            raise ValueError(f"Column '{column_name}' not found in the DataFrame")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        data[column_name].plot(ax=ax)
        ax.set_ylabel(column_name)
        ax.set_xlabel('Date')
        ax.set_title(f'Historical data for {ticker} - {column_name}')
        ax.legend(loc='best')
        return fig
