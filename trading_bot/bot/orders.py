from binance.exceptions import BinanceAPIException, BinanceOrderException
from trading_bot.bot.logging_config import logger

def place_futures_order(client, symbol, side, order_type, quantity, price=None, stop_price=None):
    """
    Places a futures order (Market, Limit, or Stop-Limit).
    
    :param client: The Binance client instance.
    :param symbol: Trading symbol (e.g., BTCUSDT).
    :param side: BUY or SELL.
    :param order_type: MARKET, LIMIT, or STOP_MARKET.
    :param quantity: Quantity to trade.
    :param price: Required for LIMIT and STOP_LIMIT orders.
    :param stop_price: Required for STOP_LIMIT and STOP_MARKET orders.
    """
    try:
        symbol = symbol.upper()
        side = side.upper()
        order_type = order_type.upper()

        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }

        # Logic for different order types
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders.")
            params['price'] = str(price)
            params['timeInForce'] = 'GTC'

        elif order_type == 'STOP_MARKET':
            if stop_price is None:
                raise ValueError("Stop Price is required for STOP_MARKET orders.")
            params['stopPrice'] = str(stop_price)
            
        elif order_type == 'STOP':
             # This is commonly referred to as STOP_LIMIT in some contexts
             if price is None or stop_price is None:
                 raise ValueError("Both Price and Stop Price are required for STOP (Stop-Limit) orders.")
             params['price'] = str(price)
             params['stopPrice'] = str(stop_price)
             params['timeInForce'] = 'GTC'

        logger.info(f"Submitting {order_type} {side} order: {params}")
        
        # Execute the order on Futures account
        response = client.futures_create_order(**params)
        
        logger.info(f"Order Success Response: {response}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: {e.status_code} - {e.message}")
        return {"error": f"API Error: {e.message}"}
    except BinanceOrderException as e:
        logger.error(f"Binance Order Exception: {e.message}")
        return {"error": f"Order Error: {e.message}"}
    except Exception as e:
        logger.error(f"Unexpected error in order placement: {str(e)}")
        return {"error": str(e)}
