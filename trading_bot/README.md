# 🚀 Binance Futures Trading Bot (Testnet)

This is a professional Python CLI trading bot designed for the **Binance Futures Testnet (USDT-M)**. It features a modular structure, robust error handling, and structured logging.

## 📁 Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py         # Binance API client wrapper
│   ├── orders.py         # Order placement logic (MARKET, LIMIT, STOP-LIMIT)
│   ├── validators.py     # Input parameters validation
│   └── logging_config.py # Centralized logging setup
├── cli.py                # Main CLI entry point
├── .env                  # Environment secrets (API Keys)
├── requirements.txt      # Project dependencies
└── README.md             # This guide
```

## 🛠️ Setup Instructions

1. **Clone the repository** and navigate to the project root.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Keys**:
   Create a `.env` file in the root directory (or update the existing one):
   ```text
   BINANCE_API_KEY=your_testnet_api_key
   BINANCE_API_SECRET=your_testnet_api_secret
   ```
   *Get your keys from [https://testnet.binancefuture.com](https://testnet.binancefuture.com)*.

## 🚀 Usage Examples

Run the bot using the `trading_bot/cli.py` script.

### 1. Market Order
```bash
python trading_bot/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### 2. Limit Order
```bash
python trading_bot/cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 2500
```

### 3. Stop-Limit Order (Bonus Property)
```bash
python trading_bot/cli.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.01 --price 65000 --stop_price 64800
```

## 📝 Logging & Validation
- **Logs**: All API requests and responses are recorded in `logs/trading.log`.
- **Validation**: The bot validates quantities, prices, and symbols before sending requests to Binance.
- **Error Handling**: Handles API network errors, insufficient balance, and invalid parameters gracefully without crashing.

## 📋 Deliverables Note
Sample logs for MARKET and LIMIT orders can be found in the `logs/` directory after execution.

---
**Assumptions**: 
- Users have a valid Binance Testnet account.
- The system has Python 3.7+ installed.
