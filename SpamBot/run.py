import os
from src.main import run_bot
from dotenv import load_dotenv, set_key

load_dotenv()
TOKEN = os.getenv("TOKEN")

if __name__ == "__main__":
    if not TOKEN: 
        inputToken = input("Token isn't found. Enter the token: ").strip()
        set_key(".env", "TOKEN", inputToken)
        TOKEN = inputToken
    try:
        run_bot(TOKEN)    
    except Exception as e:
        print(e)
        inputToken = input("Token isn't found. Enter the token: ").strip()
        set_key(".env", "TOKEN", inputToken)
        TOKEN = inputToken