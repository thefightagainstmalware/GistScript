import requests, re, datetime, time

DISCORD_WEBHOOK_REGEX = re.compile(
    r"(https?:\/\/(ptb\.|canary\.)?discord(app)?\.com\/api\/webhooks\/(\d{18})\/([\w\-]{68}))"
)

with open("gists.txt") as f:
    PASTEBINS = f.read().splitlines()


def delete_webhook(webhook: str) -> None:
    with open("404.txt", "r+") as f:
        if webhook in f.read().splitlines():
            return
        f.write(webhook + "\n")
    resp = requests.post(
        webhook,
        json={
            "content": "We are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us.",
            "tts": True,
            "username": "Anonymous via vive la revolution and The Fight Against Malware",
            "avatar_url": "https://cdn.discordapp.com/icons/910733698452815912/8dd25417b5c2a2cf49e1b98a74a15aa8.webp?size=96",
        },
        headers={
            "User-Agent": "AntiMalwareBot/gistscript (+https://discord.gg/TWhrmZFXqb)"
        },
    )
    print(resp)
    print(requests.delete(webhook))

for pastebin in PASTEBINS:
    resp = requests.get(pastebin)
    if resp.status_code != 200:
        print("Error: " + str(resp.status_code))
        continue
    for webhook in DISCORD_WEBHOOK_REGEX.findall(resp.text):
        delete_webhook(webhook[0])
    time.sleep(5)