VALID_SIDES = ('BUY', 'SELL')
VALID_ORDER_TYPES = ('MARKET', 'LIMIT', 'STOP_MARKET')


def validate_inputs(symbol, side, order_type, quantity, price=None, stop_price=None):
    errors = []

    if not symbol or not isinstance(symbol, str):
        errors.append("symbol is required")
    else:
        symbol = symbol.upper().strip()

    side = side.upper() if side else ''
    if side not in VALID_SIDES:
        errors.append(f"side must be one of {VALID_SIDES}")

    order_type = order_type.upper() if order_type else ''
    if order_type not in VALID_ORDER_TYPES:
        errors.append(f"order_type must be one of {VALID_ORDER_TYPES}")

    try:
        qty = float(quantity)
        if qty <= 0:
            errors.append("quantity must be > 0")
    except (TypeError, ValueError):
        errors.append("quantity must be a valid number")
        qty = None

    parsed_price = None
    if order_type == 'LIMIT':
        if price is None:
            errors.append("price is required for LIMIT orders")
        else:
            try:
                parsed_price = float(price)
                if parsed_price <= 0:
                    errors.append("price must be > 0")
            except (TypeError, ValueError):
                errors.append("price must be a valid number")

    parsed_stop = None
    if order_type == 'STOP_MARKET':
        if stop_price is None:
            errors.append("stop_price is required for STOP_MARKET orders")
        else:
            try:
                parsed_stop = float(stop_price)
                if parsed_stop <= 0:
                    errors.append("stop_price must be > 0")
            except (TypeError, ValueError):
                errors.append("stop_price must be a valid number")

    if errors:
        raise ValueError("Validation failed:\n  - " + "\n  - ".join(errors))

    return {
        'symbol': symbol,
        'side': side,
        'order_type': order_type,
        'quantity': qty,
        'price': parsed_price,
        'stop_price': parsed_stop,
    }
