
import tweepy
import requests
import random
import time
import os

# Load keys from environment
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_SECRET,
    ACCESS_TOKEN,
    ACCESS_SECRET
)

api = tweepy.API(auth)

def get_token():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    r = requests.get(url)
    data = r.json()

    pairs = data.get("pairs", [])

    if not pairs:
        return None

    token = random.choice(pairs[:20])

    return {
        "symbol": token["baseToken"]["symbol"],
        "ca": token["baseToken"]["address"],
        "mc": token.get("fdv", 0)
    }

def make_post(token):

    size = round(random.uniform(0.2, 1.0), 2)

    message = f"""
🍌 TRADE ALERT — ENTRY

${token['symbol']}

📍 CA:
{token['ca']}

💰 Size: {size} SOL
💎 MC: ${token['mc']}

🎯 TP: 2x | SL: -50%

🤖 Auto-detected
"""

    return message.strip()

while True:

    token = get_token()

    if token:

        tweet = make_post(token)

        try:
            api.update_status(tweet)
            print("Posted:", tweet)

        except Exception as e:
            print("Error:", e)

    time.sleep(1800)
