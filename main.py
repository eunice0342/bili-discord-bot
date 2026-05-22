```python
import requests
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

UID = "1669328690"
WEBHOOK_URL = "https://discord.com/api/webhooks/1507307962341920778/8azUfvvjKPu5JQ3KJlsaPCPoBZ2H35stkxD4TvZ9SW8Q8Pq3K4BhyerGdpTCftua8Zdu"

STATE_FILE = "last_dynamic.json"

url = f"https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?host_mid={UID}"

def get_latest():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    item = data["data"]["items"][0]

    dynamic_id = item["id_str"]

    text = ""

    try:
        text = item["modules"]["module_dynamic"]["desc"]["text"]
    except:
        text = "新动态"

    return dynamic_id, text

def load_last():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)["id"]
    except:
        return None

def save_last(dynamic_id):
    with open(STATE_FILE, "w") as f:
        json.dump({"id": dynamic_id}, f)

while True:
    try:
        dynamic_id, text = get_latest()

        last_id = load_last()

        if dynamic_id != last_id:
            webhook = DiscordWebhook(url=WEBHOOK_URL)

            embed = DiscordEmbed(
                title="Bilibili 新动态",
                description=text,
                color="5865F2"
            )

            embed.set_url(f"https://t.bilibili.com/{dynamic_id}")

            webhook.add_embed(embed)
            webhook.execute()

            save_last(dynamic_id)

            print("发送成功")

    except Exception as e:
        print(e)

    time.sleep(60)
```
