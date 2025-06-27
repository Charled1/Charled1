"""Handles adaptation and learning for the trading system."""

from dataclasses import dataclass
from typing import Any

from .strategy_optimizer import StrategyOptimizer
from utils.telegram_utils import TelegramBot

@dataclass
class LearningOrganization:
    optimizer: StrategyOptimizer
    telegram: TelegramBot
    chat_id: int
    current_strategy: Any = None
    pending_strategy: Any = None

    def weekly_meeting(self) -> None:
        """Propose a new strategy and request user approval."""
        self.pending_strategy = self.optimizer.optimize()
        message = (
            f"Yeni strateji bulundu: {self.pending_strategy}.\n"
            "Uygulansın mı?"
        )
        self.telegram.send_strategy_prompt(self.chat_id, message)
        self.telegram.on_strategy_decision = self._apply_decision

    def _apply_decision(self, approve: bool) -> None:
        if approve:
            self.current_strategy = self.pending_strategy
        self.pending_strategy = None

