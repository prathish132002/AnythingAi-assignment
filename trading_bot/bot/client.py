import os
from binance.client import Client
from trading_bot.bot.logging_config import logger

class BinanceFuturesClient:
    """Class-based wrapper for Binance Futures API calls (Testnet)."""

    def __init__(self, api_key, api_secret):
        """Initializes the Binance client and points it to the Testnet."""
        # Note: python-binance handles Testnet URLs automatically when testnet=True
        # For Futures USDT-M Testnet, it uses: https://testnet.binancefuture.com/fapi
        self.client = Client(api_key, api_secret, testnet=True)
        # Explicit override to ensure it points to the correct Futures Testnet base
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi/v1'
        
        logger.info(f"Binance Futures Client initialized. Base URL: {self.client.FUTURES_URL}")

    def get_futures_client(self):
        return self.client
