from email.mime import image
import requests
import os
import json
import math
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

# This is where you add the collection name to the URL
CollectionName = "Collection Name".lower()

# Random User Agent
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
user_agent = user_agent_rotator.get_random_user_agent()

# Headers for the request. Currently this is generating random user agents
# Use a custom header version here -> https://www.whatismybrowser.com/guides/the-latest-user-agent/
headers = {
      'User-Agent': user_agent,
      "Accept": "application/json"
  }

# Get information regarding collection

collection = requests.get(f"http://api.opensea.io/api/v1/collection/{CollectionName}?format=json")

if collection.status_code == 429:
    print("Server returned HTTP 429. Request was throttled. Please try again in about 5 minutes.")

if collection.status_code == 404:
    print("NFT Collection not found.\n\n(Hint: Try changing the name of the collection in the Python script, line 6.)")
    exit()

collectioninfo = json.loads(collection.content.decode())

# Create image folder if it doesn't exist.

if not os.path.exists('./images'):
    os.mkdir('./images')

if not os.path.exists(f'./images/{CollectionName}'):
    os.mkdir(f'./images/{CollectionName}')

if not os.path.exists(f'./images/{CollectionName}/image_data'):
    os.mkdir(f'./images/{CollectionName}/image_data')

# Get total NFT count

count = int(collectioninfo["collection"]["stats"]["count"])

# Opensea limits to 50 assets per API request, so here we do the division and round up.

iter = math.ceil(count / 50)

print(f"\nBeginning download of \"{CollectionName}\" collection.\n")

# Define variables for statistics

stats = {
  "DownloadedData": 0,
  "AlreadyDownloadedData": 0,
  "DownloadedImages": 0,
  "AlreadyDownloadedImages": 0,
  "FailedImages": 0
}

# Define IPFS Gateways

ipfs_gateways = [
'cf-ipfs.com', 
'gateway.ipfs.io', 
'cloudflare-ipfs.com', 
'10.via0.com', 
'gateway.pinata.cloud', 
'ipfs.cf-ipfs.com', 
'ipfs.io', 
'ipfs.sloppyta.co', 
'ipfs.best-practice.se', 
'snap1.d.tube', 
'ipfs.greyh.at', 
'ipfs.drink.cafe', 
'ipfs.2read.net', 
'robotizing.net', 
'dweb.link', 
'ninetailed.ninja'
]

# Create IPFS download function
def ipfs_resolve(image_url):
  cid = image_url.removeprefix("ipfs://")
  for gateway in ipfs_gateways:
    request = requests.get(f"https://{gateway}/ipfs/{cid}")
    if request.status_code == 200:
      break
  return request

# Iterate through every unit
for i in range(iter):
    offset = i * 50
    data = json.loads(requests.get(f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={offset}&limit=50&collection={CollectionName}&format=json", headers=headers).content.decode())

    if "assets" in data:
        for asset in data["assets"]:
          formatted_number = f"{int(asset['token_id']):04d}"

          print(f"\n#{formatted_number}:")

          # Check if data for the NFT already exists, if it does, skip saving it
          if os.path.exists(f'./images/{CollectionName}/image_data/{formatted_number}.json'):
              print(f"  Data  -> [\u2713] (Already Downloaded)")
              stats["AlreadyDownloadedData"] += 1
          else:
                # Take the JSON from the URL, and dump it to the respective file.
                dfile = open(f"./images/{CollectionName}/image_data/{formatted_number}.json", "w+")
                json.dump(asset, dfile, indent=3)
                dfile.close()
                print(f"  Data  -> [\u2713] (Successfully downloaded)")
                stats["DownloadedData"] += 1

          # Check if image already exists, if it does, skip saving it
          if os.path.exists(f'./images/{CollectionName}/{formatted_number}.png'):
              print(f"  Image -> [\u2713] (Already Downloaded)")
              stats["AlreadyDownloadedImages"] += 1
          else:
            # Make the request to the URL to get the image
            if not asset["image_original_url"] == None:
              image_url = asset["image_original_url"]
            else:
              image_url = asset["image_url"]
            
            # If the URL returned is IPFS, then change it to use a public gateway
            if image_url.startswith("ipfs://"):
              image_url = ipfs_resolve(image_url).url
              image = requests.get(image_url)

            # If the URL returns status code "200 Successful", save the image into the "images" folder.
            if image.status_code == 200:
                file = open(f"./images/{CollectionName}/{formatted_number}.png", "wb+")
                file.write(image.content)
                file.close()
                print(f"  Image -> [\u2713] (Successfully downloaded)")
                stats["DownloadedImages"] += 1
            # If the URL returns a status code other than "200 Successful", alert the user and don't save the image
            else:
                print(f"  Image -> [!] (HTTP Status {image.status_code})")
                stats["FailedImages"] += 1
                continue

print(f"""

Finished downloading collection.


Statistics
-=-=-=-=-=-

Total of {count} units in collection "{CollectionName}".

Downloads:

  JSON Files ->
    {stats["DownloadedData"]} successfully downloaded
    {stats["AlreadyDownloadedData"]} already downloaded

  Images ->
    {stats["DownloadedImages"]} successfully downloaded
    {stats["AlreadyDownloadedImages"]} already downloaded
    {stats["FailedImages"]} failed


You can find the images in the images/{CollectionName} folder.
The JSON for each NFT can be found in the images/{CollectionName}/image_data folder.
Press enter to exit...""")
input()
