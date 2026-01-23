from fyers_apiv3 import fyersModel
from dotenv import load_dotenv
from auth import generate_new_token
import pandas as pd
import time
import os
# import subprocess
# import sys


load_dotenv()

def get_fyers_instance(token):
    client_id = os.getenv("CLIENT_ID")
    return fyersModel.FyersModel(client_id = client_id, token=token, log_path ="")

def check_token_validity(fyers):
    try:
        response =fyers.get_profile()
        return response.get('s') == 'ok'
    except Exception:
        return False

def fetch_data(fyers):
    # data = {"symbol":"NSE:NIFTY50-INDEX", "strikecount":5}
    data = {"symbols":"NSE:NIFTY50-INDEX"}
    response = fyers.quotes(data)
    print('working.....1')
    if response.get('s') == 'ok'and response.get('d'):
        print('working.....2')
        nifty_data = response['d'][0]['v']
        print('working.....3')
        lp = nifty_data.get('lp')
        print(f'Nifty price today = {lp}')

        # df = pd.DataFrame(response['data']['optionChain'])
        # print(df[['strike_price', 'option_type', 'lp', 'oi']])
        return lp
    else:
        print("Error:", response.get('message'))
        return None
def main():

    token_file = "access_token.txt"
    max_retries = 2  # ലോഗിൻ ശ്രമങ്ങളുടെ പരിധി
    attempts = 0
    while attempts < max_retries:
        token = None
        if os.path.exists(token_file):
            with open(token_file, "r") as f:
                token = f.read().strip()
    
        if token:
            fyers = get_fyers_instance(token)
            if check_token_validity(fyers):
                print("token is valid and Fetching data......")
                try:
                    while True:
                        fetch_data(fyers)
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n🛑 പ്രോഗ്രാം യൂസർ നിർത്തി.")
                    return
                except Exception as e:
                    print(f"Error during fetching: {e}")
                    token = None
            else:
                print("❌ Token exists but is invalid/expired.")
                token = None
        
        if not token:
            print("token is expired and making new one.....")
            print("authentication file is running now .....")
            if generate_new_token():
                attempts += 1
                print("authentication executed and main file is running now.....")
                continue
            else:
                print("Authentication failed..........")
                break


if __name__ == "__main__":
    main()
