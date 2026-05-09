from typing import Optional


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol.isalnum():
        raise ValueError(f"Invalid symbol '{symbol}'. Use alphanumeric only, e.g. BTCUSDT.")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of: {', '.join(VALID_SIDES)}.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}."
        )
    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid quantity '{quantity}'. Must be a positive number.")
    if qty <= 0:
        raise ValueError(f"Quantity must be greater than zero. Got: {qty}")
    return qty


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        try:
            p = float(price)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid price '{price}'. Must be a positive number.")
        if p <= 0:
            raise ValueError(f"Price must be greater than zero. Got: {p}")
        return p
    if order_type == "STOP_MARKET":
        if price is None:
            raise ValueError("Stop price is required for STOP_MARKET orders.")
        try:
            p = float(price)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid stop price '{price}'. Must be a positive number.")
        if p <= 0:
            raise ValueError(f"Stop price must be greater than zero. Got: {p}")
        return p
    return None  # MARKET orders don't need a price


def validate_all(symbol: str, side: str, order_type: str, quantity: str, price: Optional[str]):
    """Run all validations and return clean values."""
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)
    return symbol, side, order_type, quantity, price
