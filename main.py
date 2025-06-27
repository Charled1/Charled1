"""Entry point for running a minimal trading bot demo."""

import logging
import pandas as pd

from utils.indicator_utils import IndicatorCalculator
from utils.data_utils import DataProcessor
from utils.risk_utils import RiskManager
from utils.telegram_utils import TelegramBot, TelegramFormatter
from utils.config_utils import ConfigManager

from core.trading_ceo import MasterpieceCEO
from core.position_manager import PositionManager
from core.strategy_optimizer import StrategyOptimizer
from core.learning_organization import LearningOrganization


def main() -> None:
    """Instantiate system components and execute a simple workflow."""

    cfg = ConfigManager().load()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    indicator_calc = IndicatorCalculator()
    data_processor = DataProcessor()
    risk_manager = RiskManager(
        account_balance=cfg["risk"]["account_balance"],
        risk_percent=cfg["risk"].get("risk_percent", 1.0),
        max_daily_loss_percent=cfg["risk"].get("max_daily_loss_percent", 5.0),
    )
    telegram = TelegramFormatter()

    # Core managers
    ceo = MasterpieceCEO(
        indicator_calc=indicator_calc,
        data_processor=data_processor,
        risk_manager=risk_manager,
        telegram=telegram,
    )
    telegram_bot = TelegramBot(
        token=cfg["telegram"]["token"],
        on_start=ceo.start,
        on_stop=ceo.shutdown,
    )
    position_manager = PositionManager(risk_manager=risk_manager, telegram=telegram)
    optimizer = StrategyOptimizer()
    learning_org = LearningOrganization(
        optimizer=optimizer,
        telegram=telegram_bot,
        chat_id=cfg["telegram"]["chat_id"],
    )

    telegram_bot.start_polling()

    # Fetch recent OHLCV data for demonstration
    data = data_processor.fetch_ohlcv("BTC/USDT", timeframe="1h", limit=50)
    ceo.strategy_meeting(data)

    # Open a sample position and run a mock optimization cycle
    position_manager.open_position("BTCUSDT", entry=100, stop=95, target=110)
    learning_org.weekly_meeting()


if __name__ == "__main__":
    main()

