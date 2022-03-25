import requests, re, datetime, time

DISCORD_WEBHOOK_REGEX = re.compile(
    r"(https?:\/\/(ptb\.|canary\.)?discord(app)?\.com\/api\/webhooks\/(\d{18})\/([\w\-]{68}))"
)
ID_EXTRACTOR = re.compile(r"\/.{32}\/")

with open("gists.txt") as f:
    GISTS = f.read().splitlines()


def delete_webhook(webhook):
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
    requests.delete(webhook)


GIST_IDS = [ID_EXTRACTOR.search(gist).group(0)[1:-1] for gist in GISTS]

last_updated = {gist: 0 for gist in GIST_IDS}

while True:
    for gist in GIST_IDS:
        data = requests.get(f"https://api.github.com/gists/{gist}").json()
        ts = datetime.datetime.strptime(
            data["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
        ).timestamp()
        if ts > last_updated[gist]:
            last_updated[gist] = ts
            for file in data["files"]:
                matches = DISCORD_WEBHOOK_REGEX.finditer(data["files"][file]["content"])
                for match in matches:
                    delete_webhook(match.group(0))
    time.sleep(60)
