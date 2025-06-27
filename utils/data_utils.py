"""Data validation and cleaning utilities."""

from dataclasses import dataclass
import logging
import pandas as pd
from typing import Optional

import ccxt

@dataclass
class DataProcessor:
    """Validates and cleans raw OHLCV data."""

    def fill_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.fillna(method='ffill').fillna(method='bfill')

    def fix_ohlc_relations(self, df: pd.DataFrame) -> pd.DataFrame:
        df['high'] = df[['open', 'close', 'high']].max(axis=1)
        df['low'] = df[['open', 'close', 'low']].min(axis=1)
        return df

    def calculate_data_quality_score(self, df: pd.DataFrame) -> float:
        total = len(df)
        missing = df.isna().sum().sum()
        score = max(0, 100 - (missing / (total * len(df.columns))) * 100)
        return round(score, 2)

    def fetch_ohlcv(
        self, symbol: str, timeframe: str = "1h", limit: int = 100, exchange: Optional[str] = "binance"
    ) -> pd.DataFrame:
        """Fetch OHLCV data from an exchange using ccxt."""
        try:
            exchange_class = getattr(ccxt, exchange)
            ex = exchange_class()
            raw = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)
            return df
        except Exception as exc:
            logging.error("Failed to fetch OHLCV: %s", exc)
            return pd.DataFrame()

