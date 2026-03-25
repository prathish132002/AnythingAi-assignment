from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import os
import sys
from dotenv import load_dotenv

# Ensure the root directory is in sys.path for internal imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.orders import place_futures_order
from trading_bot.bot.validators import validate_symbol, validate_positive_float
from trading_bot.bot.logging_config import logger

app = FastAPI(title="Binance Futures Bot Dashboard")

# Setup templates and static files
# Note: Since we are in the root of the project, we'll look for 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load environment variables
load_dotenv()
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"api_key_status": bool(API_KEY)})

@app.post("/api/order")
async def place_order(
    symbol: str = Form(...),
    side: str = Form(...),
    order_type: str = Form(...),
    quantity: float = Form(...),
    price: float = Form(None),
    stop_price: float = Form(None)
):
    if not API_KEY or not API_SECRET:
        raise HTTPException(status_code=400, detail="API Keys missing in .env")

    try:
        # Initialize Client
        bot_client_wrapper = BinanceFuturesClient(API_KEY, API_SECRET)
        client = bot_client_wrapper.get_futures_client()
        
        # Place Order
        response = place_futures_order(
            client=client,
            symbol=symbol.upper(),
            side=side.upper(),
            order_type=order_type.upper(),
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        
        if "error" in response:
            return JSONResponse(status_code=400, content={"status": "error", "message": response["error"]})
        
        return JSONResponse(content={"status": "success", "data": response})

    except Exception as e:
        logger.error(f"Web Order Failed: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/api/logs")
async def get_logs():
    try:
        log_file = "logs/trading.log"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                lines = f.readlines()
                return {"logs": lines[-50:]} # Return last 50 logs
        return {"logs": ["No logs found."]}
    except Exception as e:
        return {"logs": [f"Error reading logs: {e}"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
