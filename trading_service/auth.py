from fyers_apiv3 import fyersModel
from dotenv import load_dotenv
import os
import webbrowser
# import urllib.parse as urlparse

load_dotenv()

def generate_new_token():
    client_id = os.getenv("CLIENT_ID")
    secret_key = os.getenv("SECRET_KEY")
    redirect_url = os.getenv("REDIRECT_URL") 

    session = fyersModel.SessionModel(
        client_id = client_id,
        secret_key = secret_key,
        redirect_uri = redirect_url,
        response_type="code",
        grant_type="authorization_code"
        )                                               

    auth_url = session.generate_authcode()
    print(f" the auth url = {auth_url}")
    webbrowser.open(auth_url)

    response_url = input("paste the generated URL here...")
    # auth_code = response_url.split('auth_code=')[1].split('&')[0]
    # print(f" the auth code.......... = {auth_code}")

    try:
        auth_code = response_url.split('auth_code=')[1].split('&')[0]
        print(f" the auth code.......... = {auth_code}")

        if auth_code:
            # print(f"authentication code generated: {response_url}")

            # 5. ലഭിച്ച auth_code ഉപയോഗിച്ച് ആക്സസ് ടോക്കൺ ഉണ്ടാക്കുന്നു
            session.set_token(auth_code)
            response = session.generate_token()
            if 'access_token' in response:
                new_token = response['access_token']
                fyers = fyersModel.FyersModel(client_id=client_id, token=new_token, log_path="")
                profile = fyers.get_profile()

                if profile.get('s') == 'ok':
                    with open("access_token.txt","w") as f:
                        f.write(new_token)
            
                    print(f"✅ Login Success! Welcome {profile.get('data', {}).get('name')}")
                    return True
                else:
                    error_msg = profile.get('message', 'Validation Failed')
                    print(f"❌ API Error (Token): {error_msg}")
                    print(f"DEBUG: Full Response from Fyers: {profile}")
                    return False
            else:
                error_message = response.get('message', 'Check Secret Key or Client ID')
                print(f"❌ API Error: {error_message}")          
                return False
    
    except Exception as e:
        print(f"Error: check the URL link......({str(e)})")
        return False

        