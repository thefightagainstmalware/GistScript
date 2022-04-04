# GistScript
Sometimes, malware developers hide their webhooks in GitHub Gists, allowing the victims of the malware to still get their session ID's stolen even if the original webhook is long gone. This script automates the process of checking the GitHub gists and deleting any webhooks found
## How to contribute
If you want to add a new gist, add it to the bottom of `gists.txt`, and file a pull request.

## Running locally
Running locally is simple!
```sh
python -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
Update with `git pull`
