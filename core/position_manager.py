"""Manages open trading positions."""

from dataclasses import dataclass, field
import logging
from typing import List

from utils.risk_utils import RiskManager
from utils.telegram_utils import TelegramFormatter

@dataclass
class Position:
    symbol: str
    entry: float
    stop: float
    target: float

@dataclass
class PositionManager:
    risk_manager: RiskManager
    telegram: TelegramFormatter
    active_positions: List[Position] = field(default_factory=list)

    def open_position(self, symbol: str, entry: float, stop: float, target: float):
        size = self.risk_manager.calculate_position_size(abs(entry - stop))
        pos = Position(symbol, entry, stop, target)
        self.active_positions.append(pos)
        logging.info(self.telegram.format_position_open(symbol, entry))
        return size

    def close_position(self, symbol: str) -> None:
        """Close a position and notify."""
        self.active_positions = [p for p in self.active_positions if p.symbol != symbol]
        logging.info("Position closed on %s", symbol)

