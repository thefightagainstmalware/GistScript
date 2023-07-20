# GistScript
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a><br>
Sometimes, malware developers hide their webhooks in various pastebin services, allowing the victims of the malware to still get their session IDs stolen even if the original webhook is long gone. This script automates the process of checking the pastebins and deleting any webhooks found
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
