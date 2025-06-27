class PositionManager:
    """Manages opening and closing positions via a ccxt exchange instance."""

    def __init__(self, exchange):
        self.exchange = exchange
        self.positions = {}
        self.orders = {}

    def place_order(self, symbol, side, amount, price=None, order_type="market", params=None):
        """Submit an order through the exchange and store the result."""
        params = params or {}
        if order_type not in {"market", "limit", "stop"}:
            raise ValueError(f"Unsupported order type: {order_type}")
        if order_type != "market" and price is None:
            raise ValueError(f"{order_type.capitalize()} order requires price")

        order = self.exchange.create_order(symbol, order_type, side, amount, price, params)
        self.orders[order["id"]] = order
        return order

    def cancel_order(self, order_id, symbol):
        """Cancel an order on the exchange and update internal state."""
        result = self.exchange.cancel_order(order_id, symbol)
        if order_id in self.orders:
            self.orders[order_id]["status"] = result.get("status", "canceled")
        return result

    def open_position(self, symbol, side, amount, price=None, order_type="market", params=None):
        """Place an order to open a position and record its ID."""
        order = self.place_order(symbol, side, amount, price, order_type, params)
        self.positions[symbol] = {
            "side": side,
            "amount": amount,
            "order_id": order["id"],
        }
        return order

    def close_position(self, symbol, amount=None, price=None, order_type="market", params=None):
        """Close an existing position using a new order."""
        if symbol not in self.positions:
            raise ValueError(f"No open position for symbol: {symbol}")
        pos = self.positions[symbol]
        side = "sell" if pos["side"] == "buy" else "buy"
        amount = amount or pos["amount"]
        order = self.place_order(symbol, side, amount, price, order_type, params)
        pos["close_order_id"] = order["id"]
        return order
