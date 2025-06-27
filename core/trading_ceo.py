"""Main coordinator for the trading system."""

from dataclasses import dataclass, field
import logging
from typing import List
import pandas as pd

from utils.indicator_utils import IndicatorCalculator
from utils.data_utils import DataProcessor
from utils.risk_utils import RiskManager
from utils.telegram_utils import TelegramFormatter

@dataclass
class MasterpieceCEO:
    indicator_calc: IndicatorCalculator
    data_processor: DataProcessor
    risk_manager: RiskManager
    telegram: TelegramFormatter
    watchlist: List[str] = field(default_factory=list)

    def start(self):
        if self.risk_manager.check_kill_switch():
            logging.error("Cannot start: kill switch active")
            return
        message = "Sistem başlatıldı"
        logging.info(self.telegram.format_scanner_update(message))

    def shutdown(self):
        message = "Sistem durduruldu"
        logging.info(self.telegram.format_scanner_update(message))

    def strategy_meeting(self, data: pd.DataFrame):
        cleaned = self.data_processor.fill_missing(data)
        score = self.data_processor.calculate_data_quality_score(cleaned)
        if score < 50:
            logging.warning(self.telegram.send_emergency_notification("Data quality low"))
            return
        # This is where indicator calculations and strategy logic would go.

    def operations_monitoring(self):
        # Placeholder for continuous operations
        pass

