#!/usr/bin/env python3
import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from bot.orders import place_order
from bot.logging_config import setup_logger

logger = setup_logger()


def get_credentials():
    key = os.getenv('BINANCE_API_KEY', '').strip()
    secret = os.getenv('BINANCE_API_SECRET', '').strip()
    if not key or not secret:
        print("[ERROR] Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET in .env or env vars.")
        sys.exit(1)
    return key, secret


def build_parser():
    p = argparse.ArgumentParser(
        description='Binance Futures Testnet Trading Bot',
        formatter_class=argparse.RawTextHelpFormatter
    )
    p.add_argument('--symbol', required=True, help='Trading pair, e.g. BTCUSDT')
    p.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='BUY or SELL')
    p.add_argument('--type', dest='order_type', required=True,
                   choices=['MARKET', 'LIMIT', 'STOP_MARKET'], help='Order type')
    p.add_argument('--quantity', required=True, help='Order quantity')
    p.add_argument('--price', default=None, help='Limit price (required for LIMIT orders)')
    p.add_argument('--stop-price', dest='stop_price', default=None,
                   help='Stop price (required for STOP_MARKET orders)')
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    api_key, api_secret = get_credentials()

    try:
        place_order(
            api_key=api_key,
            api_secret=api_secret,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except (ValueError, RuntimeError):
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
