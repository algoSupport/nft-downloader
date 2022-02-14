# NFT Downloader
The sole purpose of this script is to download any NFT collection from [OpenSea](https://opensea.io).

## Setup
Prerequisites:
- Python 3
- Python `requests` library (Install using `pip install requests`)
- Python `random_user_agents` library (Install using `pip install random_user_agent`)
- A brain

To download the script, either use `git clone` or click "Code" > "Download ZIP" on the GitHub page.

Lastly, open the script in a text editor, and change the `CollectionName` variable on Line 11 to your collection of choice, by finding the collection's name on OpenSea. For example, the [Lazy Lions](https://opensea.io/collection/lazy-lions) collection has the name "lazy-lions" (opensea.io/collection/**lazy-lions**). CollectionName can also be found in the URL on opensea.io

Now, just run the script.

On Linux, just type `python3 opensea.py` in the terminal.

On Windows, just double-click on the file.

On MacOS, there are many different ways to do it. ([Google it](https://google.com/?q=how+to+open+python+script+on+macos))

## How does it work?
Basically, the OpenSea website allows for scripts like this one to reach into their system via an API. Using this API, we fetch the amount of items in the collection of choice, and split it into 50-item chunks each, and start downloading them. Everything is automated, except for setting the name of the collection.
