"""Formatting helpers for Telegram notifications."""

from dataclasses import dataclass
from typing import Callable, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, Updater)

@dataclass
class TelegramFormatter:
    """Creates formatted strings for Telegram notifications."""

    def format_position_open(self, symbol: str, price: float) -> str:
        return f"🚀 Position opened on {symbol} at {price:.2f}"

    def format_scanner_update(self, message: str) -> str:
        return f"📈 {message}"

    def send_emergency_notification(self, message: str) -> str:
        return f"❗️ EMERGENCY: {message}"


class TelegramBot:
    """Simple wrapper around python-telegram-bot to manage commands."""

    def __init__(
        self,
        token: str,
        on_start: Optional[Callable[[], None]] = None,
        on_stop: Optional[Callable[[], None]] = None,
        on_strategy_decision: Optional[Callable[[bool], None]] = None,
    ) -> None:
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.on_start = on_start
        self.on_stop = on_stop
        self.on_strategy_decision = on_strategy_decision

        self.running = False

        self.dispatcher.add_handler(CommandHandler("start", self._cmd_start))
        self.dispatcher.add_handler(CommandHandler("stop", self._cmd_stop))
        self.dispatcher.add_handler(CallbackQueryHandler(self._button_handler))

    def _cmd_start(self, update: Update, context: CallbackContext) -> None:
        self.running = True
        if self.on_start:
            self.on_start()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bot başlatıldı")

    def _cmd_stop(self, update: Update, context: CallbackContext) -> None:
        self.running = False
        if self.on_stop:
            self.on_stop()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Bot durduruldu")

    def _button_handler(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        if query.data == "accept_strategy":
            if self.on_strategy_decision:
                self.on_strategy_decision(True)
            query.edit_message_text("Strateji onaylandı")
        elif query.data == "reject_strategy":
            if self.on_strategy_decision:
                self.on_strategy_decision(False)
            query.edit_message_text("Strateji reddedildi")

    def send_strategy_prompt(self, chat_id: int, message: str) -> None:
        keyboard = [
            [
                InlineKeyboardButton("Evet", callback_data="accept_strategy"),
                InlineKeyboardButton("Hayır", callback_data="reject_strategy"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        self.updater.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

    def send_message(self, chat_id: int, message: str) -> None:
        self.updater.bot.send_message(chat_id=chat_id, text=message)

    def start_polling(self) -> None:
        self.updater.start_polling()

    def stop_polling(self) -> None:
        self.updater.stop()

