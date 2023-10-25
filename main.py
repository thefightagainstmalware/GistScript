import requests, re, time, base64, sys, urllib.parse, os

DISCORD_WEBHOOK_REGEX = re.compile(
    r"https?:\/\/(?:ptb\.|canary\.)?discord(?:app)?\.com\/api(?:\/)?(v\d{1,2})?\/webhooks\/\d{17,21}\/[\w\-]{68}"
)

BASE64_REGEX = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?")

debug = "--debug" in sys.argv


def debug_print(*args, **kwargs):
    if debug:
        print(*args, **kwargs)
    if os.getenv("GISTSCRIPT_LOGGING_WEBHOOK"):
        requests.post(os.getenv("GISTSCRIPT_LOGGING_WEBHOOK"), json={"content": " ".join(args)})


def delete_webhook(webhook: str, log: "str | None" = None) -> None:
    with open("404.txt", "r+") as f:
        if webhook in f.read().splitlines():
            return
        f.write(webhook + "\n")

    if log:
        r = requests.get(webhook)
        if r.status_code == 200:
            requests.post(log, json={"content": r.text})

    resp = requests.post(
        webhook,
        json={
            "content": "反病毒软件战争万岁！！！！！！！！！！！！！！",
            "tts": True,
            "username": "The Fight Against Malware",
            "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Ukraine.svg/1920px-Flag_of_Ukraine.svg.png",
        },
        headers={
            "User-Agent": "AntiMalwareBot/gistscript (+https://discord.gg/TWhrmZFXqb)"
        },
    )
    debug_print(resp)
    if resp.status_code == 404:
        return
    debug_print(requests.delete(webhook))


def run(pastebins, logging_webhook=None):
    for pastebin in pastebins:
        try:
            resp = requests.get(
                pastebin,
                headers={
                    "User-Agent": "AntiMalwareBot/gistscript (+https://discord.gg/TWhrmZFXqb)"
                },
            )
        except Exception as e:
            print(f"Error: {e} on {pastebin}")
            continue
        if resp.status_code != 200:
            print(f"Error: {resp.status_code} on {pastebin}")
            continue

        oldtext = resp.text
        text = resp.text
        icanhasbase64 = BASE64_REGEX.match(text)
        while (
            icanhasbase64 is not None
            and icanhasbase64.start() == 0
            and icanhasbase64.end() == len(text)
        ):  # screw you, massileQOL
            debug_print(f"Base64 detected on url ({pastebin}), decoding...")
            try:
                text = base64.b64decode(text).decode("utf-8")
            except UnicodeDecodeError as e:
                debug_print("not base64")
                text = oldtext
                break
            debug_print("Decoded: " + text)
            icanhasbase64 = BASE64_REGEX.match(text)

        text = urllib.parse.unquote(text)
        for webhook in DISCORD_WEBHOOK_REGEX.finditer(text):
            debug_print(webhook.group(0))
            delete_webhook(webhook.group(0), logging_webhook)


webhook = os.getenv("GISTSCRIPT_LOGGING_WEBHOOK")


with open("gists.txt") as f:
    PASTEBINS = f.read().splitlines()

if "--oneoff" in sys.argv:
    run(PASTEBINS, webhook)
    sys.exit(0)

while True:
    run(PASTEBINS, webhook)
    time.sleep(5)
