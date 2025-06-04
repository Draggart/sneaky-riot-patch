import snscrape.modules.twitter as sntwitter
import requests

USERNAME = "RiotPhroxzon"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1379947155497947246/RysJfkp61_SnP_BPAFKNfR4Hcn8lDFv9pBEHNEJx-tCGM4b2lzjKa8wJNahHb2CnYAn5"  # pon el tuyo
KEYWORDS = ["patch", "preview"]

def get_latest_tweet():
    for tweet in sntwitter.TwitterUserScraper(USERNAME).get_items():
        if any(keyword.lower() in tweet.content.lower() for keyword in KEYWORDS):
            return tweet
        break
    return None

def main():
    try:
        with open("last_tweet.txt", "r") as f:
            last_seen_id = f.read().strip()
    except FileNotFoundError:
        last_seen_id = ""

    tweet = get_latest_tweet()
    if not tweet:
        print("❌ No se pudo obtener tweet")
        return

    if str(tweet.id) == last_seen_id:
        print("ℹ️ Tweet ya enviado antes")
        return

    data = {
        "content": f"https://x.com/{USERNAME}/status/{tweet.id}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("✅ Enviado a Discord")

        with open("last_tweet.txt", "w") as f:
            f.write(str(tweet.id))
    else:
        print(f"❌ Error al enviar a Discord: {response.status_code}")

if __name__ == "__main__":
    main()


