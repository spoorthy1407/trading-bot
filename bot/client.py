import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger

BASE_URL = "https://demo-fapi.binance.com"
logger = setup_logger("client")


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-MBX-APIKEY": self.api_key,
                "Content-Type": "application/json",
            }
        )

    # ------------------------------------------------------------------ #
    #  Signing                                                             #
    # ------------------------------------------------------------------ #
    def _sign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    # ------------------------------------------------------------------ #
    #  Generic request helper                                              #
    # ------------------------------------------------------------------ #
    def _request(self, method: str, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = BASE_URL + endpoint
        signed_params = self._sign(params)

        logger.debug("REQUEST  %s %s  params=%s", method.upper(), endpoint, signed_params)

        try:
            resp = self.session.request(method, url, params=signed_params, timeout=10)
            logger.debug("RESPONSE status=%s  body=%s", resp.status_code, resp.text)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as exc:
            try:
                err_body = exc.response.json()
            except Exception:
                err_body = exc.response.text
            logger.error("HTTP error %s — %s", exc.response.status_code, err_body)
            raise RuntimeError(
                f"Binance API error {exc.response.status_code}: {err_body}"
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            logger.error("Network failure: %s", exc)
            raise RuntimeError(f"Network failure: {exc}") from exc
        except requests.exceptions.Timeout:
            logger.error("Request timed out for %s %s", method, endpoint)
            raise RuntimeError("Request timed out. Check your connection.") from None

    # ------------------------------------------------------------------ #
    #  Public helpers                                                      #
    # ------------------------------------------------------------------ #
    def get_account_info(self) -> Dict[str, Any]:
        return self._request("GET", "/fapi/v2/account", {})

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: str = "GTC",
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force

        if order_type == "STOP_MARKET":
            params["stopPrice"] = stop_price

        return self._request("POST", "/fapi/v1/order", params)
