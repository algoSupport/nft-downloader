# OpenSea NFT Stealer
The sole purpose of this script is to download any NFT collection from [OpenSea](https://opensea.io).

## Setup
Prerequisites:
- Python 3
- A brain

To download the script, either use `git clone` or click "Code" > "Download ZIP" on the GitHub page.

Lastly, open the script in a text editor, and change the `CollectionName` variable on Line 11 to your collection of choice, by finding the collection's name on OpenSea. For example, the [Lazy Lions](https://opensea.io/collection/lazy-lions) collection has the name "lazy-lions" (opensea.io/collection/**lazy-lions**).

## How does it work?
Basically, the OpenSea website allows for scripts like this one to reach into their system via an API. Using this API, we fetch the amount of items in the collection of choice, and split it into 50-item chunks each, and start downloading them. Everything is automated, except for setting the name of the collection.

## Why did you make this?
2 reasons: Firstly, for the funny. Secondly, out of spite for these stupid [#RightClickVictim](https://mobile.twitter.com/hashtag/RightClickVictim)s. I'm tired of all these NFT junkies constantly talking about how they're victims to screenshotting, and how screenshotting is property theft. So to rub salt in their exaggerated wounds, here is a script that downloads literally every NFT in any collection on the most popular NFT trading website.
