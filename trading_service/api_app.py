import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi import Depends
from main import get_fyers_instance, check_token_validity, fetch_data
from auth import generate_new_token

app = FastAPI(title="NSE Trading Bot API")

# def verify_access(fyers=Depends(get_valid_fyers)):
#     if not fyers:
#         return RedirectResponse(url="/login")

def get_valid_fyers():
    token_file = "access_token.txt"
    if not os.path.exists(token_file):
        return None
    
    try:
        with open(token_file, "r") as f:
            token = f.read().strip()
        if not token:
            return None
        fyers = get_fyers_instance(token)

        if check_token_validity(fyers):
            return fyers
        else:
            return None
    except Exception as e:
        print(f"Error reading tokeen: {e}")
        return None

@app.get("/")
def home():
    fyers = get_valid_fyers()
    if not fyers:
      return RedirectResponse(url="/login") 
    return {"status": "Online", "message":"Nifty Bot API is running"}

@app.get("/login")
def login():
    fyers = get_valid_fyers()
    if fyers:
        return RedirectResponse(url="/price")
    print("Starting login Process. Check your terminal to pase the URL.")
    if generate_new_token():
        return {"message":"Login successfull"}
    return {"message":"Login failed"}

@app.get("/price")
def get_price():
    fyers = get_valid_fyers()
    if not fyers:
      return RedirectResponse(url="/login")  
    
    data = fetch_data(fyers)
    return {"symbol":"NIFTY 50","lp":data}

@app.get("/stocks")
def get_stocks():
    return [
        {"symbol": "NSE:RELIANCE-EQ", "price": random.randint(2400, 2600)},
        {"symbol": "NSE:TCS-EQ", "price": random.randint(3300, 3500)}
    ]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
