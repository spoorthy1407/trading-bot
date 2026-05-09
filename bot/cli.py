#!/usr/bin/env python3
"""
Trading Bot CLI — Binance Futures Testnet
Usage examples:
  python -m bot.cli --symbol BTCUSDT --side BUY  --type MARKET --quantity 0.01
  python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT  --quantity 0.01 --price 50000
  python -m bot.cli --symbol ETHUSDT --side BUY  --type STOP_MARKET --quantity 0.1 --price 2000
"""

import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.logging_config import setup_logger
from bot.orders import place_order
from bot.validators import validate_all

load_dotenv()
logger = setup_logger("cli")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading-bot",
        description="Place orders on Binance Futures Testnet",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--symbol",   required=True,  help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",     required=True,  help="BUY or SELL")
    parser.add_argument("--type",     required=True,  dest="order_type", help="MARKET, LIMIT, or STOP_MARKET")
    parser.add_argument("--quantity", required=True,  help="Order quantity, e.g. 0.01")
    parser.add_argument("--price",    required=False, default=None,
                        help="Limit price (required for LIMIT) or stop price (required for STOP_MARKET)")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # ---- Load API credentials from env -------------------------------- #
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        print("\n❌  BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file.\n")
        logger.error("Missing API credentials in environment.")
        sys.exit(1)

    # ---- Validate inputs ---------------------------------------------- #
    try:
        symbol, side, order_type, quantity, price = validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValueError as exc:
        print(f"\n❌  Validation error: {exc}\n")
        logger.warning("Validation failed: %s", exc)
        sys.exit(1)

    # ---- Place order -------------------------------------------------- #
    client = BinanceClient(api_key=api_key, api_secret=api_secret)
    try:
        place_order(client, symbol, side, order_type, quantity, price)
    except RuntimeError:
        sys.exit(1)


if __name__ == "__main__":
    main()
