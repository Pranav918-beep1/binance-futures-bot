from .client import BinanceClient
from .validators import validate_inputs
from .logging_config import setup_logger

logger = setup_logger()


def place_order(api_key, api_secret, symbol, side, order_type, quantity, price=None, stop_price=None):
    # validate first
    try:
        params = validate_inputs(symbol, side, order_type, quantity, price, stop_price)
    except ValueError as e:
        logger.error(str(e))
        raise

    print("\n--- Order Request ---")
    print(f"  Symbol    : {params['symbol']}")
    print(f"  Side      : {params['side']}")
    print(f"  Type      : {params['order_type']}")
    print(f"  Quantity  : {params['quantity']}")
    if params['price']:
        print(f"  Price     : {params['price']}")
    if params['stop_price']:
        print(f"  Stop Price: {params['stop_price']}")
    print("---------------------")

    logger.info(f"Placing {params['order_type']} {params['side']} order | "
                f"symbol={params['symbol']} qty={params['quantity']}"
                + (f" price={params['price']}" if params['price'] else "")
                + (f" stopPrice={params['stop_price']}" if params['stop_price'] else ""))

    client = BinanceClient(api_key, api_secret)

    try:
        resp = client.place_order(
            symbol=params['symbol'],
            side=params['side'],
            order_type=params['order_type'],
            quantity=params['quantity'],
            price=params['price'],
            stop_price=params['stop_price'],
        )
    except RuntimeError as e:
        logger.error(f"Order failed: {e}")
        print(f"\n[FAILED] {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n[ERROR] {e}")
        raise

    # print response summary
    order_id = resp.get('orderId', 'N/A')
    status = resp.get('status', 'N/A')
    exec_qty = resp.get('executedQty', '0')
    avg_price = resp.get('avgPrice', resp.get('price', 'N/A'))
    # orig_qty = resp.get('origQty')  # not needed for display but keep for debug

    print("\n--- Order Response ---")
    print(f"  Order ID    : {order_id}")
    print(f"  Status      : {status}")
    print(f"  Executed Qty: {exec_qty}")
    print(f"  Avg Price   : {avg_price}")
    print("----------------------")
    print("[SUCCESS] Order placed successfully!\n")

    logger.info(f"Order placed | orderId={order_id} status={status} executedQty={exec_qty} avgPrice={avg_price}")

    return resp
