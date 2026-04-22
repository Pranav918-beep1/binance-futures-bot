import hashlib
import hmac
import time
import requests
from urllib.parse import urlencode
from .logging_config import setup_logger

BASE_URL = 'https://testnet.binancefuture.com'
logger = setup_logger()


class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    def _sign(self, params: dict) -> dict:
        params['timestamp'] = int(time.time() * 1000)
        query = urlencode(params)
        sig = hmac.new(self.secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        params['signature'] = sig
        return params

    def _post(self, endpoint, params):
        signed = self._sign(params)
        url = BASE_URL + endpoint
        logger.debug(f"POST {url} | params: { {k: v for k, v in signed.items() if k != 'signature'} }")
        try:
            resp = self.session.post(url, data=signed, timeout=10)
            data = resp.json()
            logger.debug(f"Response [{resp.status_code}]: {data}")
            if not resp.ok:
                code = data.get('code', resp.status_code)
                msg = data.get('msg', 'unknown error')
                raise RuntimeError(f"API error {code}: {msg}")
            return data
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network error: {e}")
            raise
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }

        if order_type == 'LIMIT':
            params['price'] = price
            params['timeInForce'] = 'GTC'
        elif order_type == 'STOP_MARKET':
            params['stopPrice'] = stop_price

        return self._post('/fapi/v1/order', params)
