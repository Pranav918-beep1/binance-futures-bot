# Binance Futures Testnet Trading Bot

Simple CLI bot for placing futures orders on Binance testnet (USDT-M only). Built for the Primetrade assignment.

# Setup

You'll need Python 3.8+ and a testnet account. Go to https://testnet.binancefuture.com and login with GitHub — it'll auto-create an account. Then grab your API key from the dashboard.

> Note: if you're in India or SEA the testnet URL might redirect to main binance site. Use a VPN if that happens.

install deps:
```bash
pip install -r requirements.txt
```

copy the env file and fill in your keys:
```bash
cp .env.example .env
```

`.env` should look like:
```
BINANCE_API_KEY=xxxx
BINANCE_API_SECRET=xxxx
```

# Running it

**Market order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Limit order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 66000
```

**Stop-market (bonus):**
```bash
python cli.py --symbol ETHUSDT --side SELL --type STOP_MARKET --quantity 0.1 --stop-price 2950
```

both BUY and SELL work for all order types, just swap `--side`.

---

## What the output looks like

```
--- Order Request ---
  Symbol    : BTCUSDT
  Side      : BUY
  Type      : MARKET
  Quantity  : 0.001
---------------------

--- Order Response ---
  Order ID    : 3892710234
  Status      : FILLED
  Executed Qty: 0.001
  Avg Price   : 64821.30
----------------------
[SUCCESS] Order placed successfully!
```

errors print inline and also get logged to file.

---

## Project structure

```
trading_bot/
  bot/
    client.py         # handles signing + raw API calls
    orders.py         # order logic, prints summary
    validators.py     # input checks b4 hitting the API
    logging_config.py
  cli.py
  logs/bot.log
  .env.example
  requirements.txt
```

---

## Logs

Everything goes to `logs/bot.log` — requests, responses, errors. Rotates at 5MB.

Sample:
```
2025-04-18 10:14:02 [INFO] Placing MARKET BUY order | symbol=BTCUSDT qty=0.001
2025-04-18 10:14:03 [INFO] Order placed | orderId=3892710234 status=FILLED executedQty=0.001 avgPrice=64821.30
```

<!-- TODO: maybe add a flag to disable file logging if not needed -->

---

## Assumptions / notes

- USDT-M futures only, COIN-M not supported
- testnet URL is hardcoded, don't use this on mainnet as-is
- LIMIT orders default to GTC
- no balance check before placing — testnet gives you virtual funds anyway
* error handling covers validation errors, API errors, and network failures

---

## Requirements

just two:
```
requests
python-dotenv
```
