"""Risk management utilities."""

from dataclasses import dataclass
from typing import Optional
import logging
import os

@dataclass
class RiskManager:
    account_balance: float
    risk_percent: float = 1.0
    max_daily_loss_percent: float = 5.0
    daily_loss: float = 0.0
    kill_switch_file: str = "KILL_SWITCH.txt"

    def calculate_position_size(self, stop_distance: float) -> float:
        risk_amount = self.account_balance * (self.risk_percent / 100)
        return risk_amount / max(stop_distance, 1e-10)

    def check_daily_drawdown(self, realized_loss: float) -> bool:
        self.daily_loss += realized_loss
        over_limit = self.daily_loss > self.account_balance * (self.max_daily_loss_percent / 100)
        if over_limit:
            logging.warning("Daily loss limit exceeded: %.2f", self.daily_loss)
        return over_limit

    def check_kill_switch(self) -> bool:
        active = os.path.exists(self.kill_switch_file)
        if active:
            logging.error("Kill switch activated")
        return active

    def reset_daily_loss(self) -> None:
        self.daily_loss = 0.0

