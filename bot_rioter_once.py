import subprocess
import json
import requests
import os

RIOTER_USERNAME = "RiotPhroxzon"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1379947155497947246/RysJfkp61_SnP_BPAFKNfR4Hcn8lDFv9pBEHNEJx-tCGM4b2lzjKa8wJNahHb2CnYAn5"
KEYWORDS = ["patch", "preview"]
LAST_TWEET_FILE = "last_tweet.txt"

def get_last_seen_id():
    if os.path.exists(LAST_TWEET_FILE):
        with open(LAST_TWEET_FILE, "r") as f:
            return f.read().strip()
    return ""

def set_last_seen_id(tweet_id):
    with open(LAST_TWEET_FILE, "w") as f:
        f.write(tweet_id)

def get_latest_tweet(username):
    cmd = f'snscrape --jsonl --max-results 1 twitter-user "{username}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        tweet_data = json.loads(result.stdout.strip().split("\n")[0])
        return {
            "id": tweet_data["id"],
            "url": tweet_data["url"],
            "content": tweet_data["content"]
        }
    return None

def send_to_discord(tweet):
    data = {
        "username": "Sneaky Patch",
        "embeds": [{
            "title": "Nuevo tweet detectado",
            "description": tweet["content"],
            "url": tweet["url"],
            "color": 0x1DA1F2
        }]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def tweet_contains_keywords(tweet_text):
    return any(kw.lower() in tweet_text.lower() for kw in KEYWORDS)

def main():
    tweet = get_latest_tweet(RIOTER_USERNAME)
    if tweet:
        last_seen_id = get_last_seen_id()
        if tweet["id"] != last_seen_id and tweet_contains_keywords(tweet["content"]):
            send_to_discord(tweet)
            set_last_seen_id(tweet["id"])
            print(f"Tweet enviado: {tweet['url']}")
        else:
            print("Sin tweets nuevos o sin palabras clave.")
    else:
        print("No se pudo obtener tweet.")

if __name__ == "__main__":
    main()
