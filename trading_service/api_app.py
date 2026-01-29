import os
import uvicorn
import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
import main 
import auth
import db_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s"
)
logger = logging.getLogger("TradingBot")

app = FastAPI(title="NSE Trading Bot API")

@app.on_event("startup")
def startup_event():
    db_manager.int_db()
    logger.info("Database initialized")

def get_valid_fyers():
    token = db_manager.get_token()
    if not token:
        return None
    fyers = main.get_fyers_instance(token)
    return fyers if main.check_token_validity(fyers) else None

@app.get("/")
def home():
    logger.info("Home route accessed")
    fyers = get_valid_fyers()
    if not fyers:
      return RedirectResponse(url="/login") 
    return {"status": "Online", "message":"Nifty Bot API is running"}

@app.get("/login")
def login():
    logger.info("redirecting to Fyers Login")

    return RedirectResponse( url = auth.generate_new_token_step1())

@app.get("/callback")
def callback(auth_code: str = None):
    if not auth_code:
        logger.error("No auth code in callback")
        return {"error":"Failed"}
    if auth.generate_new_token_step2(auth_code):
        logger.info("Successfully generated and saved the token")
        return RedirectResponse(url="/")
    return {"error":"Token failed"}

@app.websocket("/ws/price")
async def price_stream(webocket:WebSocket):
    await webocket.accept()
    try:
        while True:
            fyers =get_valid_fyers()
            price = main.fetch_data(fyers) if fyers else "Not Auth"
            await webocket.send_json({"nifty":price})
            await asyncio.sleep(1)
    
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")

@app.get("/price")
def get_price():
    fyers = get_valid_fyers()
    if not fyers:
      return RedirectResponse(url="/login")  
    
    data = main.fetch_data(fyers)
    return {"symbol":"NIFTY 50","data":data}

# @app.get("/stocks")
# def get_stocks():
#     return [
#         {"symbol": "NSE:RELIANCE-EQ", "price": random.randint(2400, 2600)},
#         {"symbol": "NSE:TCS-EQ", "price": random.randint(3300, 3500)}
    # ]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
