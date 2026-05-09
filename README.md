# Trading Bot — Binance Futures Testnet

A lightweight Python CLI application to place orders on [Binance Futures Testnet](https://testnet.binancefuture.com) (USDT-M).

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance REST API wrapper (signing, requests)
│   ├── orders.py          # Order placement + formatted output
│   ├── validators.py      # Input validation
│   ├── logging_config.py  # Structured logging (file + console)
│   └── cli.py             # CLI entry point (argparse)
├── logs/                  # Auto-created; stores daily log files
├── .env.example           # Template for API credentials
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/trading-bot.git
cd trading-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Binance Futures Testnet credentials

1. Visit [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Sign in with GitHub
3. Click **"API Key"** tab → generate your key pair

### 4. Configure credentials

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

---

## How to Run

### MARKET order (BUY)
```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### LIMIT order (SELL)
```bash
python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 50000
```

### STOP_MARKET order (bonus order type)
```bash
python -m bot.cli --symbol ETHUSDT --side BUY --type STOP_MARKET --quantity 0.1 --price 2000
```

### Help
```bash
python -m bot.cli --help
```

---

## Example Output

```
==================================================
         ORDER REQUEST SUMMARY
==================================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.01
==================================================

--------------------------------------------------
         ORDER RESPONSE
--------------------------------------------------
  Order ID   : 3283541
  Symbol     : BTCUSDT
  Status     : FILLED
  Side       : BUY
  Type       : MARKET
  Exec. Qty  : 0.01
  Avg Price  : 43215.60
  Time       : 1713456000000
--------------------------------------------------

✅  Order placed successfully!
```

---

## Logging

Logs are written to `logs/trading_bot_YYYYMMDD.log`.

Each log entry includes timestamp, log level, module name, and message.  
API requests, responses, and errors are all captured.

---

## Assumptions

- Testnet base URL: `https://testnet.binancefuture.com`
- All orders use default `timeInForce=GTC` for LIMIT orders
- Quantity precision should match the symbol's requirements on testnet (e.g., 0.001 BTC minimum)
- No leverage or margin configuration is set via this bot — use the testnet UI to set leverage before trading
