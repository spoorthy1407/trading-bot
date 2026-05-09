from typing import Optional

from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger("orders")


def _print_summary(symbol, side, order_type, quantity, price):
    print("\n" + "=" * 50)
    print("         ORDER REQUEST SUMMARY")
    print("=" * 50)
    print(f"  Symbol     : {symbol}")
    print(f"  Side       : {side}")
    print(f"  Type       : {order_type}")
    print(f"  Quantity   : {quantity}")
    if price is not None:
        label = "Stop Price" if order_type == "STOP_MARKET" else "Price"
        print(f"  {label:<11}: {price}")
    print("=" * 50)


def _print_response(response: dict):
    print("\n" + "-" * 50)
    print("         ORDER RESPONSE")
    print("-" * 50)
    print(f"  Order ID   : {response.get('orderId', 'N/A')}")
    print(f"  Symbol     : {response.get('symbol', 'N/A')}")
    print(f"  Status     : {response.get('status', 'N/A')}")
    print(f"  Side       : {response.get('side', 'N/A')}")
    print(f"  Type       : {response.get('type', 'N/A')}")
    print(f"  Exec. Qty  : {response.get('executedQty', 'N/A')}")
    print(f"  Avg Price  : {response.get('avgPrice', 'N/A')}")
    print(f"  Time       : {response.get('updateTime', 'N/A')}")
    print("-" * 50)


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
):
    _print_summary(symbol, side, order_type, quantity, price)

    logger.info(
        "Placing %s %s order | symbol=%s qty=%s price=%s",
        side,
        order_type,
        symbol,
        quantity,
        price,
    )

    try:
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price if order_type == "LIMIT" else None,
            stop_price=price if order_type == "STOP_MARKET" else None,
        )
        _print_response(response)
        logger.info("Order placed successfully | orderId=%s status=%s", response.get("orderId"), response.get("status"))
        print("\n✅  Order placed successfully!\n")
        return response

    except RuntimeError as exc:
        logger.error("Order failed: %s", exc)
        print(f"\n❌  Order failed: {exc}\n")
        raise
