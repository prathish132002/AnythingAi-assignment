import sys
import os
import argparse
from dotenv import load_dotenv

# Ensure the root directory is in sys.path for internal imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.orders import place_futures_order
from trading_bot.bot.validators import validate_positive_float, validate_symbol
from trading_bot.bot.logging_config import logger

def main():
    """Enhanced CLI entry point for the Binance Futures Trading Bot."""
    
    # 1. Load configuration
    load_dotenv()
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    if not api_key or not api_secret:
        print("Error: BINANCE_API_KEY or BINANCE_API_SECRET missing in .env")
        return

    # 2. Parse CLI Arguments
    parser = argparse.ArgumentParser(description="🚀 Binance Futures Trading Bot (Testnet)")
    
    parser.add_argument("--symbol", type=validate_symbol, required=True, help="Symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", type=str, required=True, 
                        choices=["MARKET", "LIMIT", "STOP", "STOP_MARKET"], 
                        help="Order type (STOP is Stop-Limit)")
    parser.add_argument("--quantity", type=validate_positive_float, required=True, help="Order quantity")
    parser.add_argument("--price", type=validate_positive_float, help="Price (required for LIMIT/STOP)")
    parser.add_argument("--stop_price", type=validate_positive_float, help="Stop price (required for STOP/STOP_MARKET)")

    args = parser.parse_args()

    # 3. Specific validation for order types
    if args.type == "LIMIT" and args.price is None:
        parser.error("--price is required for LIMIT orders.")
    
    if args.type == "STOP" and (args.price is None or args.stop_price is None):
        parser.error("--price and --stop_price are required for STOP (Stop-Limit) orders.")
        
    if args.type == "STOP_MARKET" and args.stop_price is None:
        parser.error("--stop_price is required for STOP_MARKET orders.")

    # 4. Initialize Client
    try:
        bot_client_wrapper = BinanceFuturesClient(api_key, api_secret)
        client = bot_client_wrapper.get_futures_client()
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        print(f"Failed to initialize Binance Client: {e}")
        return

    # 5. Place Order
    print(f"\n--- Order Request Summary ---")
    print(f"Symbol: {args.symbol}")
    print(f"Side:   {args.side}")
    print(f"Type:   {args.type}")
    print(f"Qty:    {args.quantity}")
    if args.price: print(f"Price:  {args.price}")
    if args.stop_price: print(f"Stop:   {args.stop_price}")
    print("-----------------------------\n")

    response = place_futures_order(
        client=client,
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stop_price
    )

    # 6. Display Result
    if "error" in response:
        print(f"❌ Order Failed: {response['error']}")
        print("Check logs/trading.log for more details.")
    else:
        print(f"✅ Order Placed Successfully!")
        print(f"Order ID:      {response.get('orderId')}")
        print(f"Status:        {response.get('status')}")
        print(f"Executed Qty:  {response.get('executedQty')}")
        print(f"Avg Price:     {response.get('avgPrice', 'N/A')}")
        print(f"Client OrderId: {response.get('clientOrderId')}")

if __name__ == "__main__":
    main()
